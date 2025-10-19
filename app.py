"""
Professional Flask API for Diabetes Prediction
Provides REST endpoints for model inference and health recommendations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import json
import os
from datetime import datetime
from functools import lru_cache

# Import XGBoost at module level for CPU inference
import xgboost as xgb

# XGBoost Booster Wrapper (needed for model loading - CPU optimized)
class XGBoostBoosterWrapper:
    """Wraps an xgboost.Booster to provide sklearn-like predict/predict_proba methods for CPU inference."""
    def __init__(self, booster):
        self.booster = booster

    def predict(self, X):
        """Predict class labels (0 or 1)"""
        dmat = xgb.DMatrix(X)
        proba = self.booster.predict(dmat)
        return (proba > 0.5).astype(int)

    def predict_proba(self, X):
        """Predict class probabilities"""
        dmat = xgb.DMatrix(X)
        proba = self.booster.predict(dmat)
        return np.column_stack([1 - proba, proba])

app = Flask(__name__)

# Optimized CORS for production
CORS(app, 
     resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     max_age=3600)

# Response compression for faster transfers
app.config['COMPRESS_MIMETYPES'] = ['application/json', 'text/html', 'text/css', 'application/javascript']
app.config['COMPRESS_LEVEL'] = 6
app.config['COMPRESS_MIN_SIZE'] = 500

# Configuration - Railway uses api/ as root, local dev uses parent directory
BASE_DIR = Path(__file__).parent
if (BASE_DIR / "diabetes_model.joblib").exists():
    # Railway deployment - model in same directory as app.py
    MODEL_PATH = BASE_DIR / "diabetes_model.joblib"
    METADATA_PATH = BASE_DIR / "model_metadata.json"
else:
    # Local development - model in parent/models directory
    MODEL_PATH = BASE_DIR.parent / "models" / "diabetes_model.joblib"
    METADATA_PATH = BASE_DIR.parent / "models" / "model_metadata.json"

# Load model and metadata
print("🔄 Loading model...")
try:
    # Register XGBoostBoosterWrapper in __main__ namespace for joblib
    import sys
    sys.modules['__main__'].XGBoostBoosterWrapper = XGBoostBoosterWrapper
    
    model_data = joblib.load(MODEL_PATH)
    MODEL = model_data['model']
    SCALER = model_data['scaler']
    FEATURES = model_data['features']
    FEATURE_IMPORTANCE = model_data.get('feature_importance', {})
    METRICS = model_data['metrics']
    MODEL_NAME = model_data['model_name']
    print(f"✅ Model loaded: {MODEL_NAME}")
    print(f"✅ Accuracy: {METRICS.get('accuracy', 0):.4f}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    MODEL = None
    SCALER = None
    FEATURES = None
    FEATURE_IMPORTANCE = {}
    METRICS = {}
    MODEL_NAME = "Not loaded"

# AI recommendations use evidence-based fallback (no external API dependencies)
print("✅ Using evidence-based recommendation system")

# Feature descriptions for better recommendations
FEATURE_DESCRIPTIONS = {
    'HighBP': 'High Blood Pressure',
    'HighChol': 'High Cholesterol',
    'CholCheck': 'Cholesterol Check in 5 years',
    'BMI': 'Body Mass Index',
    'Smoker': 'Smoking Status',
    'Stroke': 'History of Stroke',
    'HeartDiseaseorAttack': 'Heart Disease or Attack',
    'PhysActivity': 'Physical Activity in past 30 days',
    'Fruits': 'Fruit Consumption',
    'Veggies': 'Vegetable Consumption',
    'HvyAlcoholConsump': 'Heavy Alcohol Consumption',
    'AnyHealthcare': 'Has Healthcare Coverage',
    'NoDocbcCost': 'Could not see doctor because of cost',
    'GenHlth': 'General Health (1-5)',
    'MentHlth': 'Mental Health (days)',
    'PhysHlth': 'Physical Health (days)',
    'DiffWalk': 'Difficulty Walking',
    'Sex': 'Sex (0=Female, 1=Male)',
    'Age': 'Age Category',
    'Education': 'Education Level',
    'Income': 'Income Level'
}

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    response = jsonify({
        'name': 'Diabetes Prediction API',
        'version': '1.0.0',
        'status': 'running',
        'model': MODEL_NAME if MODEL else 'not loaded',
        'endpoints': {
            'health': '/health',
            'model_info': '/model-info',
            'predict': '/predict (POST)',
            'batch_predict': '/batch-predict (POST)',
            'feature_importance': '/feature-importance'
        }
    })
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    response = jsonify({
        'status': 'healthy',
        'model': MODEL_NAME if MODEL else 'not loaded',
        'model_accuracy': float(METRICS.get('accuracy', 0)) if MODEL else 0,
        'timestamp': datetime.now().isoformat()
    })
    response.headers['Cache-Control'] = 'no-cache'
    return response

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get model information and metrics"""
    if not MODEL:
        return jsonify({'error': 'Model not loaded'}), 500
    
    response = jsonify({
        'model_name': MODEL_NAME,
        'features': FEATURES,
        'feature_count': len(FEATURES),
        'feature_importance': FEATURE_IMPORTANCE,
        'metrics': {k: float(v) for k, v in METRICS.items()},
        'feature_descriptions': FEATURE_DESCRIPTIONS
    })
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction with AI-powered recommendations"""
    if not MODEL:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({
                'error': 'Missing features in request',
                'expected_format': {
                    'features': {f: 0 for f in FEATURES}
                }
            }), 400
        
        # Validate features
        input_features = data['features']
        missing_features = [f for f in FEATURES if f not in input_features]
        
        if missing_features:
            return jsonify({
                'error': 'Missing required features',
                'missing': missing_features,
                'required': FEATURES
            }), 400
        
        # Prepare input data
        input_df = pd.DataFrame([input_features])
        input_df = input_df[FEATURES]  # Ensure correct order
        
        # Scale features
        input_scaled = SCALER.transform(input_df)
        
        # Make prediction
        prediction = int(MODEL.predict(input_scaled)[0])
        prediction_proba = MODEL.predict_proba(input_scaled)[0].tolist() if hasattr(MODEL, 'predict_proba') else None
        
        # Calculate confidence
        confidence = max(prediction_proba) if prediction_proba else None
        
        # Determine risk level
        risk_level = "High Risk" if prediction == 1 else "Low Risk"
        risk_percentage = (prediction_proba[1] * 100) if prediction_proba else None
        
        # Get risk factors
        risk_factors = get_risk_factors(input_features)
        
        # Generate evidence-based recommendations (no external API calls)
        recommendations = generate_base_recommendations(features=input_features, prediction=prediction, risk_factors=risk_factors)
        
        # Prepare response
        response = {
            'prediction': prediction,
            'prediction_label': risk_level,
            'risk_percentage': risk_percentage,
            'confidence': confidence,
            'probabilities': {
                'no_diabetes': prediction_proba[0] if prediction_proba else None,
                'diabetes': prediction_proba[1] if prediction_proba else None
            },
            'risk_factors': risk_factors,
            'recommendations': recommendations,
            'model_name': MODEL_NAME,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500

def get_risk_factors(features):
    """Identify key risk factors from input"""
    risk_factors = []
    
    # Check critical risk factors
    if features.get('HighBP', 0) == 1:
        risk_factors.append({
            'factor': 'High Blood Pressure',
            'severity': 'high',
            'description': 'Elevated blood pressure increases diabetes risk'
        })
    
    if features.get('HighChol', 0) == 1:
        risk_factors.append({
            'factor': 'High Cholesterol',
            'severity': 'high',
            'description': 'High cholesterol is associated with diabetes'
        })
    
    bmi = features.get('BMI', 0)
    if bmi >= 30:
        risk_factors.append({
            'factor': f'High BMI ({bmi})',
            'severity': 'critical',
            'description': 'Obesity significantly increases diabetes risk'
        })
    elif bmi >= 25:
        risk_factors.append({
            'factor': f'Overweight BMI ({bmi})',
            'severity': 'moderate',
            'description': 'Being overweight increases diabetes risk'
        })
    
    if features.get('HeartDiseaseorAttack', 0) == 1:
        risk_factors.append({
            'factor': 'Heart Disease',
            'severity': 'high',
            'description': 'Cardiovascular disease is linked to diabetes'
        })
    
    if features.get('PhysActivity', 0) == 0:
        risk_factors.append({
            'factor': 'Low Physical Activity',
            'severity': 'moderate',
            'description': 'Lack of exercise increases diabetes risk'
        })
    
    if features.get('Smoker', 0) == 1:
        risk_factors.append({
            'factor': 'Smoking',
            'severity': 'high',
            'description': 'Smoking increases diabetes risk by 30-40%'
        })
    
    gen_health = features.get('GenHlth', 3)
    if gen_health >= 4:
        risk_factors.append({
            'factor': 'Poor General Health',
            'severity': 'moderate',
            'description': 'Poor health status correlates with diabetes'
        })
    
    return risk_factors

def generate_base_recommendations(features, prediction, risk_factors):
    """Generate evidence-based recommendations"""
    recommendations = {
        'ai_generated': False,
        'emergency_note': get_emergency_note(prediction, risk_factors),
        'lifestyle': [],
        'medical': [],
        'nutrition': [],
        'exercise': []
    }
    
    # Lifestyle recommendations
    if features.get('Smoker', 0) == 1:
        recommendations['lifestyle'].append(
            "🚭 Quit smoking - reduces diabetes risk by 30-40% within 5 years"
        )
    
    if features.get('PhysActivity', 0) == 0:
        recommendations['exercise'].append(
            "🏃 Start with 30 minutes of moderate exercise 5 days per week"
        )
        recommendations['exercise'].append(
            "💪 Include both cardio and strength training exercises"
        )
    
    bmi = features.get('BMI', 0)
    if bmi >= 25:
        recommendations['lifestyle'].append(
            f"⚖️ Weight management: Target BMI < 25 (current: {bmi})"
        )
        recommendations['nutrition'].append(
            "🥗 Follow a balanced diet with calorie deficit for weight loss"
        )
    
    # Nutrition recommendations
    recommendations['nutrition'].extend([
        "🍎 Increase fiber intake: whole grains, vegetables, fruits",
        "🥤 Limit sugary drinks and processed foods",
        "🍽️ Practice portion control and regular meal timing",
        "💧 Stay hydrated: 8-10 glasses of water daily"
    ])
    
    # Medical recommendations
    if features.get('HighBP', 0) == 1:
        recommendations['medical'].append(
            "🩺 Monitor blood pressure regularly, target <130/80 mmHg"
        )
    
    if features.get('HighChol', 0) == 1:
        recommendations['medical'].append(
            "💊 Monitor cholesterol levels, consider statin therapy if needed"
        )
    
    recommendations['medical'].extend([
        "🔬 Get HbA1c test every 3-6 months",
        "👨‍⚕️ Schedule regular check-ups with healthcare provider",
        "📊 Monitor fasting blood glucose weekly"
    ])
    
    # Exercise recommendations
    if not recommendations['exercise']:
        recommendations['exercise'].extend([
            "🚶 Walking: 10,000 steps daily",
            "🏋️ Resistance training: 2-3 times per week",
            "🧘 Yoga or stretching: stress management and flexibility"
        ])
    
    return recommendations

def get_emergency_note(prediction, risk_factors):
    """Generate emergency/urgent care notes"""
    critical_factors = [rf for rf in risk_factors if rf.get('severity') == 'critical']
    
    if prediction == 1 and len(critical_factors) > 2:
        return "⚠️ HIGH PRIORITY: Multiple critical risk factors detected. Consult a healthcare provider immediately."
    elif prediction == 1:
        return "⚠️ ELEVATED RISK: Schedule an appointment with your healthcare provider for comprehensive evaluation."
    else:
        return "✅ MAINTAIN HEALTHY HABITS: Continue preventive measures and regular health monitoring."

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """Batch prediction for multiple patients"""
    if not MODEL:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'patients' not in data:
            return jsonify({'error': 'Missing patients data'}), 400
        
        patients_data = data['patients']
        results = []
        
        for i, patient in enumerate(patients_data):
            try:
                input_df = pd.DataFrame([patient])
                input_df = input_df[FEATURES]
                input_scaled = SCALER.transform(input_df)
                
                prediction = int(MODEL.predict(input_scaled)[0])
                prediction_proba = MODEL.predict_proba(input_scaled)[0].tolist() if hasattr(MODEL, 'predict_proba') else None
                
                results.append({
                    'patient_id': i + 1,
                    'prediction': prediction,
                    'risk_level': "High Risk" if prediction == 1 else "Low Risk",
                    'confidence': max(prediction_proba) if prediction_proba else None,
                    'risk_percentage': (prediction_proba[1] * 100) if prediction_proba else None
                })
            except Exception as e:
                results.append({
                    'patient_id': i + 1,
                    'error': str(e)
                })
        
        return jsonify({
            'total_patients': len(patients_data),
            'predictions': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Batch prediction failed',
            'message': str(e)
        }), 500

@app.route('/feature-importance', methods=['GET'])
def feature_importance():
    """Get feature importance rankings"""
    if not MODEL or not FEATURE_IMPORTANCE:
        return jsonify({'error': 'Feature importance not available'}), 404
    
    return jsonify({
        'feature_importance': FEATURE_IMPORTANCE,
        'top_10': dict(list(FEATURE_IMPORTANCE.items())[:10]) if FEATURE_IMPORTANCE else {}
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Most free platforms set PORT environment variable
    # Defaults: Railway/Render/Heroku use PORT, local dev uses 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    print(f"🚀 Starting server on port {port}")
    print(f"📡 Running on: {os.environ.get('PLATFORM', 'local')}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode, threaded=True)
