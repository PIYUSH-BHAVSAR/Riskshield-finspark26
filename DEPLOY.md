# RiskShield-BFSI-X — Complete Deployment Guide

## Your GitHub Repo
```
https://github.com/PIYUSH-BHAVSAR/Riskshield-finspark26.git
```

---

## STEP 1: Push to GitHub (5 min)

### 1.1 Initialize Git & Commit All Files

```bash
cd d:\projects\finspark26

# Check git status
git status

# If not initialized:
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: RiskShield-BFSI-X with SQLite backend and React frontend"

# Add your GitHub repo
git remote add origin https://github.com/PIYUSH-BHAVSAR/Riskshield-finspark26.git

# Push to main branch
git branch -M main
git push -u origin main
```

**Expected output:**
```
Branch 'main' set up to track remote branch 'main' from 'origin'.
Everything up-to-date
```

### 1.2 Verify on GitHub
Go to: `https://github.com/PIYUSH-BHAVSAR/Riskshield-finspark26`

You should see all files uploaded ✅

---

## STEP 2: Deploy Frontend to Vercel (5 min)

### 2.1 Connect Vercel

1. Go to **[vercel.com](https://vercel.com)**
2. Click **"Import Project"**
3. Click **"From Git"**
4. Select **GitHub** (authorize if needed)
5. Search & select: `Riskshield-finspark26`
6. Click **"Import"**

### 2.2 Configure Build Settings

**In Vercel Import Dialog:**
- **Project Name:** `riskshield-frontend` (or auto-detected)
- **Framework:** `Vite`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`

### 2.3 Add Environment Variables

**Before clicking "Deploy":**

Click **"Environment Variables"** and add:

```
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co
VITE_SUPABASE_ANON_KEY=YOUR-ANON-KEY
VITE_ENVIRONMENT=production
```

**Or just use defaults** (can update later)

### 2.4 Deploy

Click **"Deploy"**

Vercel will:
- ✅ Clone your GitHub repo
- ✅ Install dependencies (`npm install`)
- ✅ Build frontend (`npm run build`)
- ✅ Deploy to CDN

**Wait 2-3 minutes...**

### 2.5 Your Frontend URL

Once deployed, you'll see:
```
🎉 Congratulations! Your project has been successfully deployed.
https://riskshield-frontend.vercel.app
```

**Copy this URL** — you'll need it for backend config

---

## STEP 3: Deploy Backend to Hugging Face Spaces (10 min)

### 3.1 Create Hugging Face Space

1. Go to **[huggingface.co/spaces](https://huggingface.co/spaces)**
2. Click **"Create new Space"**
3. Fill in:
   - **Space name:** `riskshield-bfsi-x-backend`
   - **License:** `openrail`
   - **Space type:** `Docker`
   - **Visibility:** `Public`
4. Click **"Create Space"**

### 3.2 Configure HF Space as Git Repo

HF will create an empty space with a git URL. You need to add your GitHub repo as a webhook or manually push.

**Option A: Push from GitHub (Recommended)**

```bash
# Clone your HF space (HF will show you the git URL)
git clone https://huggingface.co/spaces/YOUR-USERNAME/riskshield-bfsi-x-backend
cd riskshield-bfsi-x-backend

# Copy backend files from your project
xcopy d:\projects\finspark26\backend\* . /E /Y

# Add, commit, push
git add .
git commit -m "Deploy RiskShield backend to HF Spaces"
git push
```

**Option B: Use GitHub Actions (Automatic)**

1. In HF Space → **Settings**
2. **Linked Repo:** Connect your GitHub repo
3. HF auto-deploys on every push

### 3.3 Add Environment Variables (Secrets)

1. Go to HF Space → **Settings**
2. Scroll to **Secrets and variables**
3. Add these:

```
DATABASE_URL=sqlite:///app/riskshield.db
FRAUD_THRESHOLD=0.6
SECURITY_TRAP_THRESHOLD=1.0
CORRELATION_WINDOW_SECONDS=900
SECRET_KEY=riskshield-bfsi-x-super-secret-key
ENVIRONMENT=production
FRONTEND_URL=https://riskshield-frontend.vercel.app
```

4. Click **"Save"**

HF will auto-restart with new environment variables

### 3.4 Wait for Build

1. Go to **Logs** tab
2. Watch Docker build (takes 2-3 min)
3. Look for:
   ```
   ✅ SQLite database initialized (local)
   🚀 RiskShield-BFSI-X starting...
   Uvicorn running on http://0.0.0.0:7860
   ```

### 3.5 Your Backend URL

Once live:
```
https://YOUR-USERNAME-riskshield-bfsi-x-backend.hf.space/api/health
```

**Test it:**
```bash
curl https://YOUR-USERNAME-riskshield-bfsi-x-backend.hf.space/api/health
```

Should return:
```json
{"status":"healthy","service":"RiskShield-BFSI-X","database":"connected"}
```

---

## STEP 4: Update Frontend with Backend URL (2 min)

### 4.1 Update Vercel Environment Variable

1. Go to **Vercel Dashboard** → Your project
2. **Settings** → **Environment Variables**
3. Find `VITE_API_URL`
4. Change value to: `https://YOUR-USERNAME-riskshield-bfsi-x-backend.hf.space`
5. Click **Save**

Vercel auto-redeploys with new URL ✅

### 4.2 Verify in Frontend

Open: `https://riskshield-frontend.vercel.app`

Press **F12** (Developer Tools) → **Network** tab

Make API call (click button in frontend)

**Should see:**
- ✅ Request to `https://YOUR-USERNAME-riskshield-bfsi-x-backend.hf.space/api/...`
- ✅ Response with data (not 404 or CORS error)

---

## STEP 5: Verify Everything Works (5 min)

### 5.1 Test Backend Directly

```bash
# Health check
curl https://YOUR-USERNAME-riskshield-bfsi-x-backend.hf.space/api/health

# View API docs
# https://YOUR-USERNAME-riskshield-bfsi-x-backend.hf.space/docs
```

### 5.2 Test Frontend

1. Open: `https://riskshield-frontend.vercel.app`
2. Check console for errors (F12)
3. Try to fetch alerts (should work)
4. No CORS errors = ✅ Success

### 5.3 Test API Connectivity

From frontend → Backend should work:

```bash
# In browser console (F12):
fetch('https://YOUR-USERNAME-riskshield-bfsi-x-backend.hf.space/api/alerts')
  .then(r => r.json())
  .then(d => console.log(d))
```

Should log alert data ✅

---

## Your Live URLs

| Service | URL |
|---------|-----|
| **Frontend** | `https://riskshield-frontend.vercel.app` |
| **Backend API** | `https://YOUR-USERNAME-riskshield-bfsi-x-backend.hf.space` |
| **API Docs** | `https://YOUR-USERNAME-riskshield-bfsi-x-backend.hf.space/docs` |
| **GitHub Repo** | `https://github.com/PIYUSH-BHAVSAR/Riskshield-finspark26` |

---

## Continuous Deployment

### Auto-Deploy on Git Push

**Frontend (Vercel):**
```bash
cd frontend
# Make changes
git add .
git commit -m "Update: description"
git push origin main
# Vercel auto-deploys (1-2 min)
```

**Backend (HF Spaces):**
```bash
cd backend
# Make changes
git add .
git commit -m "Update: description"
git push origin main
# HF auto-deploys if linked (3-5 min)
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| **404 on backend URL** | Build failed | Check HF Logs tab |
| **CORS error on frontend** | Backend URL not updated | Update Vercel env vars |
| **Cannot find module** | Wrong directory | Ensure `Dockerfile` in backend root |
| **Build times out** | Large dependencies | Normal for first build, faster next time |
| **Frontend loads but no data** | Backend not responding | Check HF backend URL is correct |

---

## Quick Checklist

- [ ] GitHub repo created: https://github.com/PIYUSH-BHAVSAR/Riskshield-finspark26
- [ ] All code pushed to `main` branch
- [ ] Frontend deployed on Vercel
- [ ] Backend deployed on HF Spaces
- [ ] Environment variables set in both services
- [ ] Frontend URL: `https://riskshield-frontend.vercel.app`
- [ ] Backend URL: `https://YOUR-USERNAME-riskshield-bfsi-x-backend.hf.space`
- [ ] Backend health check returns 200
- [ ] Frontend loads without errors
- [ ] API calls from frontend reach backend
- [ ] No CORS errors in console

---

## Next Steps

1. **Seed Test Data**
   ```bash
   # Local only
   cd backend
   python data/seed_db.py
   ```

2. **Record Demo Video**
   - Show frontend loading
   - Show alerts page
   - Show graph view
   - Show API docs
   - Upload to YouTube

3. **Submit**
   - GitHub repo link
   - Frontend URL
   - Backend URL
   - Demo video link

---

**You're live!** 🚀
