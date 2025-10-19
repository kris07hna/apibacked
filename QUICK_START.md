# 🚀 Quick Setup Guide - GitHub & Vercel Deployment

Your project is ready to deploy! Follow these steps:

## ✅ Status
- ✓ Git repository initialized
- ✓ All files committed
- ✓ Vercel configuration added (`vercel.json`)
- ✓ Model file included
- ✓ `.gitignore` configured

## 📤 Step 1: Push to GitHub

### 1.1 Create a New Repository on GitHub
1. Go to https://github.com/new
2. **Repository name:** `diabetes-prediction-api` (or your choice)
3. **Description:** "REST API for diabetes risk prediction using XGBoost ML"
4. **Visibility:** Public (for easy Vercel deployment) or Private
5. **DO NOT** check "Add README" or any initialization options
6. Click **"Create repository"**

### 1.2 Push Your Code

Run these commands in your terminal (replace `YOUR_USERNAME` with your GitHub username):

```powershell
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/diabetes-prediction-api.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Note:** You'll be prompted to sign in to GitHub if not already authenticated.

## 🌐 Step 2: Deploy to Vercel

### Option A: One-Click Deploy (Easiest)

1. Go to https://vercel.com/new
2. Sign in with GitHub
3. Click **"Import Git Repository"**
4. Find and select your `diabetes-prediction-api` repository
5. Vercel will auto-detect Python and use `vercel.json` settings
6. Click **"Deploy"**
7. Wait 1-2 minutes ⏱️
8. Done! Your API is live at `https://your-project.vercel.app`

### Option B: CLI Deploy

```powershell
# Install Vercel CLI (requires Node.js)
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

## 🧪 Step 3: Test Your API

Replace `YOUR_URL` with your Vercel deployment URL:

```powershell
# Test health endpoint
curl https://YOUR_URL.vercel.app/health

# Test prediction
curl -X POST https://YOUR_URL.vercel.app/predict `
  -H "Content-Type: application/json" `
  -d '{\"features\": {\"HighBP\": 1, \"HighChol\": 1, \"BMI\": 28.5, \"Smoker\": 0, \"PhysActivity\": 1, \"GenHlth\": 2}}'
```

## 📝 Important Files Created

- **`vercel.json`** - Vercel deployment configuration
- **`.gitignore`** - Files to exclude from Git
- **`.vercelignore`** - Files to exclude from Vercel deployment
- **`VERCEL_DEPLOY.md`** - Detailed deployment guide
- **`README.md`** - Updated with deployment instructions

## 🔄 Making Updates

After making code changes:

```powershell
git add .
git commit -m "Your change description"
git push
```

Vercel automatically redeploys when you push to GitHub! 🎉

## 🆘 Troubleshooting

### Model not loading on Vercel?
The model file is included. If issues persist, check Vercel logs:
- Dashboard → Your Project → Deployments → Click deployment → Runtime Logs

### Port conflicts locally?
Change port in `app.py` or set environment variable:
```powershell
$env:PORT=8000; python app.py
```

### Need help?
- Check `VERCEL_DEPLOY.md` for detailed instructions
- Vercel Docs: https://vercel.com/docs
- GitHub Issues: Create an issue in your repo

## 🎯 Next Steps

1. ✅ Push to GitHub (instructions above)
2. ✅ Deploy to Vercel (instructions above)
3. 📧 Share your API URL
4. 🎨 Build a frontend (React, Vue, etc.)
5. 🔒 Add authentication (optional)
6. 📊 Add monitoring (Vercel Analytics)

---

**Ready to deploy?** Start with Step 1 above! 🚀
