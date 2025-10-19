# Diabetes Prediction API 🏥

REST API for diabetes risk prediction using XGBoost machine learning model.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/diabetes-prediction-api)

## Quick Start

**Requirements:** Python 3.11+

```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/diabetes-prediction-api.git
cd diabetes-prediction-api

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run locally
python app.py
```

API runs on `http://localhost:5000`

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Welcome message |
| `/health` | GET | API health check |
| `/model-info` | GET | Model details |
| `/predict` | POST | Single prediction |
| `/batch-predict` | POST | Multiple predictions |
| `/feature-importance` | GET | Feature importance scores |

## Example: Make Prediction

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "gender": 1,
    "bmi": 28.5,
    "blood_pressure_systolic": 130,
    "blood_pressure_diastolic": 85,
    "cholesterol": 240,
    "glucose": 120,
    "smoking": 0,
    "alcohol": 0,
    "physical_activity": 1,
    "diet_quality": 3,
    "sleep_hours": 7,
    "stress_level": 2,
    "family_history": 0,
    "hypertension": 0,
    "heart_disease": 0,
    "kidney_disease": 0,
    "thyroid_disease": 0,
    "medications": 1,
    "healthcare_access": 1,
    "education_level": 2
  }'
```

**Response:**
```json
{
  "risk_score": 0.72,
  "risk_level": "High",
  "recommendation": "Consult with healthcare provider",
  "risk_factors": ["High BMI", "High Blood Pressure", "High Glucose"],
  "emergency_note": null
}
```

## Deployment Options

### Deploy to Vercel (Recommended for Serverless)

1. **Push to GitHub** (see instructions below)
2. **Import to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel will auto-detect settings from `vercel.json`
   - Click "Deploy"

### Deploy to Render

👉 **See DEPLOY.md for full 5-minute setup guide**

## Model

- **Type:** XGBoost Classifier
- **Accuracy:** 87%
- **Features:** 20 health indicators
- **File:** `diabetes_model.joblib`

## Troubleshooting

- **Port already in use?** Change port in `app.py` or kill process: `lsof -i :5000`
- **Model not found?** Ensure `diabetes_model.joblib` in same directory
- **Connection refused?** Flask not running - restart with `python app.py`

---

**Status:** ✅ Production-ready on Render free tier
