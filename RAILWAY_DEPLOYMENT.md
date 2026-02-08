# 🚂 Railway Deployment Guide

Complete step-by-step guide to deploy your premium streaming backend to Railway.

## Prerequisites

✅ GitHub repository: `html-proof/sample-music-app` (pushed)
✅ Railway account (free tier available)
✅ Firebase service account JSON file

---

## Step 1: Create Railway Account

1. Go to https://railway.app
2. Click **"Login"** or **"Start a New Project"**
3. Sign in with **GitHub** (recommended for easy repo access)
4. Authorize Railway to access your GitHub repositories

---

## Step 2: Create New Project

1. Click **"New Project"** button
2. Select **"Deploy from GitHub repo"**
3. Choose **`html-proof/sample-music-app`**
4. Railway will detect the `Dockerfile` automatically

---

## Step 3: Configure Build Settings

Railway should auto-detect your Dockerfile. Verify:

- **Builder**: Dockerfile
- **Dockerfile Path**: `backend/Dockerfile`
- **Root Directory**: `backend/`

If not auto-detected:
1. Click **Settings** → **Build**
2. Set **Root Directory**: `backend`
3. Set **Builder**: Dockerfile

---

## Step 4: Add Redis Database

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"Add Redis"**
3. Railway automatically creates a Redis instance
4. The `REDIS_URL` environment variable is **auto-injected** into your backend service

✅ No manual configuration needed!

---

## Step 5: Configure Environment Variables

Click on your backend service → **"Variables"** tab

Add the following:

### Required Variables

```bash
# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=/app/serviceAccountKey.json
FIREBASE_PROJECT_ID=music-app-f2e65

# App Configuration (optional, has defaults)
APP_NAME=MusicApp Backend
DEBUG=False
```

### Important: Firebase Service Account

You have two options:

#### Option A: Upload as Base64 (Recommended)
1. Convert your Firebase JSON to base64:
   ```bash
   # On Windows (PowerShell)
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("path\to\serviceAccountKey.json"))
   
   # On Linux/Mac
   base64 -w 0 serviceAccountKey.json
   ```
2. Add variable: `FIREBASE_CREDENTIALS_BASE64=<base64-string>`
3. Update `app/firebase.py` to decode and use this

#### Option B: Use Railway Volumes (Advanced)
1. Create a Railway volume
2. Upload your service account JSON
3. Mount to `/app/serviceAccountKey.json`

---

## Step 6: Deploy!

1. Railway will automatically start building
2. Watch the **"Deployments"** tab for progress
3. Build process:
   - Pull base image (Python 3.11)
   - Install dependencies
   - Copy application code
   - Build complete (~3-5 minutes)

---

## Step 7: Get Your Public URL

1. Go to **Settings** → **Networking**
2. Click **"Generate Domain"**
3. Railway provides a free domain: `your-app.up.railway.app`
4. Copy this URL

---

## Step 8: Test Your Deployment

### Health Check
```bash
curl https://your-app.up.railway.app/health
```

Expected response:
```json
{"status": "healthy"}
```

### Test Stream (using test endpoint)
```bash
curl https://your-app.up.railway.app/test/stream/JGwWNGJdvx8
```

---

## Step 9: Remove Test Endpoints (Production)

⚠️ **Important**: Remove test endpoints before going live!

1. Delete `backend/app/routes/test.py`
2. Remove from `backend/app/main.py`:
   ```python
   # Remove this line
   from app.routes import ... test
   app.include_router(test.router)
   ```
3. Commit and push:
   ```bash
   git add .
   git commit -m "Remove test endpoints for production"
   git push
   ```
4. Railway auto-deploys the update

---

## Step 10: Configure CORS (if needed)

Update `backend/app/main.py` to allow your frontend domain:

```python
origins = [
    "http://localhost:3000",
    "https://your-frontend.vercel.app",  # Add your frontend URL
]
```

---

## 🎯 Final Checklist

- ✅ Railway project created
- ✅ Redis database added
- ✅ Environment variables configured
- ✅ Deployment successful
- ✅ Health check passing
- ✅ Public URL generated
- ✅ Test endpoints removed (production)
- ✅ CORS configured for frontend

---

## 📊 Monitor Your Deployment

### View Logs
1. Click **"Deployments"** tab
2. Select latest deployment
3. View real-time logs

### Check Metrics
1. Click **"Metrics"** tab
2. Monitor:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## 🔧 Troubleshooting

### Build Fails
- Check Dockerfile syntax
- Verify `requirements.txt` is complete
- Check build logs for errors

### Redis Connection Issues
- Verify Redis plugin is added
- Check `REDIS_URL` is auto-injected
- Test with in-memory fallback (should work even if Redis fails)

### Firebase Errors
- Verify service account JSON is valid
- Check `FIREBASE_PROJECT_ID` matches your project
- Ensure Firebase Admin SDK is initialized

### 500 Errors
- Check deployment logs
- Verify all environment variables are set
- Test endpoints locally first

---

## 💰 Pricing

**Free Tier Includes:**
- 500 hours/month execution time
- 512 MB RAM
- 1 GB disk
- Shared CPU

**Upgrade for:**
- More resources
- Custom domains
- Priority support

---

## 🚀 Next Steps

1. **Frontend Deployment**: Deploy your Next.js frontend to Vercel
2. **Custom Domain**: Add your own domain in Railway settings
3. **Monitoring**: Set up error tracking (Sentry, LogRocket)
4. **CI/CD**: Railway auto-deploys on every push to `main`

---

## 📝 Quick Reference

| Item | Value |
|------|-------|
| **Repository** | `html-proof/sample-music-app` |
| **Root Directory** | `backend` |
| **Port** | 8080 (auto-detected) |
| **Health Endpoint** | `/health` |
| **Redis** | Auto-configured via plugin |

---

**Your backend is now live! 🎉**

Access it at: `https://your-app.up.railway.app`
