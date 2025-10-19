# Deploy to Render in 5 Minutes 🚀

Render is the **best free platform** for this API (no model size limits, unlike Vercel).

## Step 1: Push Code to GitHub

```bash
# If not already done
git add .
git commit -m "Clean minimal API ready for production"
git push origin main
```

## Step 2: Create Render Account

1. Go to https://render.com (free tier available)
2. Sign up with GitHub account
3. Click "Connect GitHub account"

## Step 3: Create Web Service

1. Dashboard → **New+** → **Web Service**
2. Connect your `diabetes-prediction-api` repo
3. Fill in settings:
   - **Name:** `diabetes-api` (or your choice)
   - **Environment:** `Python 3.11`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 2 -b 0.0.0.0:$PORT -k sync app:app --timeout 120`
4. Click **Create Web Service**

> ⏳ First deploy takes ~2-3 minutes. Watch the logs.

## Step 4: Test Your API

Once deployed, Render gives you a URL like: `https://diabetes-api-xxxxx.onrender.com`

Test it:
```bash
# Health check
curl https://your-url.onrender.com/health

# Make prediction
curl -X POST https://your-url.onrender.com/predict \
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

## Step 5: Enable Auto-Deploy (Optional)

1. In Render dashboard, go to your service
2. Settings → **Auto-Deploy** → Toggle `ON`
3. Now every GitHub push auto-deploys

---

## Performance on Free Tier

- **CPU:** 0.5 vCPU (shared)
- **RAM:** 512 MB
- **Uptime:** 99.9%
- **Concurrent Users:** ~5-20 (depends on load)
- **Prediction Speed:** 20-50ms
- **Cost:** FREE ✅

## Troubleshooting

### Deploy fails - "Import Error"
- Check `requirements.txt` has all packages
- Verify `app.py` is in root directory

### API returns 503 error
- Service is spinning down on free tier (first request takes 30s)
- Wait a moment and retry

### Model file not found
- Ensure `diabetes_model.joblib` is in repo root
- Check file size < 500MB
- Render supports large files (unlike Vercel)

### Port issues
- Render automatically sets `$PORT` environment variable
- Code correctly uses: `os.getenv("PORT", 5000)`

---

## Pro Tips

1. **Keep model updated?** Push new `diabetes_model.joblib` to GitHub, auto-deploy will pick it up
2. **Monitor logs?** Render dashboard shows live logs in real-time
3. **Debug?** Enable Flask debug mode in `app.py` for better error messages
4. **Custom domain?** Render free tier supports custom domains (add in Settings)

---

**Estimated Time:** 5 minutes ⏱️
**Difficulty:** Easy ✅
**Cost:** FREE (0% payment required)
