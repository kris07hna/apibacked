# Deploy to Vercel - Complete Guide 🚀

## Prerequisites
- GitHub account
- Vercel account (free tier available at [vercel.com](https://vercel.com))
- Git installed on your computer

## Step 1: Upload to GitHub

### Initialize Git Repository (if not already done)

```bash
# Navigate to your project directory
cd c:\Users\krishna\apibacked

# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Diabetes prediction API"
```

### Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon in top right → **"New repository"**
3. Repository settings:
   - **Name:** `diabetes-prediction-api` (or your preferred name)
   - **Description:** "REST API for diabetes risk prediction using XGBoost ML model"
   - **Visibility:** Public or Private
   - **DO NOT** initialize with README (we already have one)
4. Click **"Create repository"**

### Push Code to GitHub

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/diabetes-prediction-api.git

# Push code to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Easiest)

1. **Sign in to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "Sign Up" or "Log In"
   - Choose "Continue with GitHub"

2. **Import Project:**
   - Click **"Add New..."** → **"Project"**
   - Click **"Import"** next to your `diabetes-prediction-api` repository
   - If you don't see it, click "Adjust GitHub App Permissions" to grant access

3. **Configure Project:**
   - **Framework Preset:** Other
   - **Root Directory:** `./` (leave default)
   - **Build Command:** (leave empty)
   - **Output Directory:** (leave empty)
   - Vercel will automatically detect Python and use `vercel.json` settings

4. **Deploy:**
   - Click **"Deploy"**
   - Wait 1-2 minutes for deployment to complete
   - You'll get a URL like: `https://diabetes-prediction-api.vercel.app`

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - What's your project's name? diabetes-prediction-api
# - In which directory is your code located? ./
# - Deploy? Yes
```

## Step 3: Test Your Deployment

### Test Health Endpoint
```bash
curl https://your-app.vercel.app/health
```

### Test Prediction Endpoint
```bash
curl -X POST https://your-app.vercel.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "HighBP": 1,
      "HighChol": 1,
      "CholCheck": 1,
      "BMI": 28.5,
      "Smoker": 0,
      "Stroke": 0,
      "HeartDiseaseorAttack": 0,
      "PhysActivity": 1,
      "Fruits": 1,
      "Veggies": 1,
      "HvyAlcoholConsump": 0,
      "AnyHealthcare": 1,
      "NoDocbcCost": 0,
      "GenHlth": 2,
      "MentHlth": 5,
      "PhysHlth": 3,
      "DiffWalk": 0,
      "Sex": 1,
      "Age": 9,
      "Education": 4,
      "Income": 6
    }
  }'
```

## Step 4: Configure Custom Domain (Optional)

1. In Vercel dashboard, go to your project
2. Click **"Settings"** → **"Domains"**
3. Add your custom domain
4. Follow DNS configuration instructions

## Troubleshooting

### Issue: "Model not found" error
**Solution:** Ensure `diabetes_model.joblib` is committed to Git:
```bash
git add diabetes_model.joblib
git commit -m "Add model file"
git push
# Redeploy in Vercel
```

### Issue: Large file size warning
**Solution:** Model files are essential. If over 100MB, use Git LFS:
```bash
git lfs install
git lfs track "*.joblib"
git add .gitattributes
git commit -m "Track large files with LFS"
```

### Issue: Deployment fails
**Solution:** Check Vercel deployment logs:
1. Go to Vercel dashboard
2. Click on your project
3. Go to "Deployments" tab
4. Click on failed deployment
5. Check "Building" and "Runtime Logs"

### Issue: Cold start delays
**Note:** Vercel's free tier has cold starts (3-5 seconds). This is normal for serverless.

## Vercel Configuration Files

The project includes these configuration files:

### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### `.vercelignore`
Excludes unnecessary files from deployment.

## Updating Your Deployment

```bash
# Make changes to your code
# Commit changes
git add .
git commit -m "Description of changes"
git push

# Vercel automatically deploys on push to main branch
```

## Environment Variables (if needed)

If you need to add secrets or config:
1. Vercel Dashboard → Your Project → **Settings** → **Environment Variables**
2. Add variables like `API_KEY`, `DATABASE_URL`, etc.
3. Redeploy

## Vercel Free Tier Limits

✅ **Included:**
- Unlimited deployments
- 100GB bandwidth/month
- Automatic HTTPS
- Global CDN
- Serverless functions

⚠️ **Limitations:**
- 10 second execution timeout
- Cold starts on infrequent requests
- Limited to hobby projects

## Support

- **Vercel Docs:** https://vercel.com/docs
- **GitHub Issues:** Create issue in your repository
- **Vercel Discord:** https://vercel.com/discord

---

**Your API will be live at:** `https://your-project-name.vercel.app` 🎉
