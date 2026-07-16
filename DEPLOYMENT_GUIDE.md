# RiskShield-BFSI-X — Complete Deployment Guide

## Architecture: Hugging Face Spaces (Backend) + Vercel (Frontend) + Supabase (DB)

```
┌─────────────────────────────────────────────────────────────┐
│                      Vercel (Frontend)                       │
│         https://riskshield-frontend.vercel.app              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  React Vite App (Dashboard, Alerts, Graph View)      │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┬──────────────────────────────────────┘
                        │ CORS: axios calls
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Hugging Face Spaces (Backend)                  │
│  https://YOUR-USERNAME-riskshield-bfsi-x.hf.space         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FastAPI + Docker                                    │   │
│  │  /api/health, /api/alerts, /api/predict, etc         │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┬──────────────────────────────────────┘
                        │ PostgreSQL Driver (psycopg2)
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Supabase PostgreSQL (Database)                 │
│  postgresql://postgres:PASSWORD@db.supabase.co:5432/postgres │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  predictions, security_events, correlated_alerts     │   │
│  │  Includes: RLS policies, audit logging, indexes      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: Backend Deployment (Hugging Face Spaces) — 10 min

### 1.1 Create Hugging Face Space

```bash
# Manual way:
1. Go to huggingface.co/spaces
2. Click "Create new Space"
3. Name: riskshield-bfsi-x
4. Type: Docker
5. Click "Create Space"
```

### 1.2 Prepare Code

```bash
cd /path/to/finspark26/backend

# Files already in place:
# ✅ app.py (FastAPI main app)
# ✅ database.py (Supabase connection)
# ✅ requirements.txt (Python dependencies)
# ✅ Dockerfile (for Hugging Face)
# ✅ HF_SPACES_README.md (deployment instructions)
```

### 1.3 Push to Hugging Face

```bash
# Initialize git if needed
git init
git add .
git commit -m "Deploy RiskShield backend to Hugging Face Spaces"

# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/YOUR-USERNAME/riskshield-bfsi-x

# Push code
git push hf main
```

### 1.4 Add Environment Variables

**Go to:** Space → Settings → Secrets and variables

Add:
```
SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co
SUPABASE_KEY=YOUR-ANON-KEY
DATABASE_URL=postgresql://postgres:Piyush%401665@db.ukoxjxfevchmfhctuqsa.supabase.co:5432/postgres
DATABASE_POOL_MAX=10
FRAUD_THRESHOLD=0.6
SECURITY_TRAP_THRESHOLD=1.0
CORRELATION_WINDOW_SECONDS=900
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
FRONTEND_URL=https://riskshield-frontend.vercel.app
```

Save → Hugging Face auto-restarts container

### 1.5 Verify Backend is Running

```bash
# Wait 2-3 min for build, then:
curl https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/health

# Should return:
# {"status":"healthy","service":"RiskShield-BFSI-X","database":"connected"}
```

**Backend API URL:** `https://YOUR-USERNAME-riskshield-bfsi-x.hf.space`

---

## Step 2: Frontend Deployment (Vercel) — 10 min

### 2.1 Prepare Frontend Code

```bash
cd /path/to/finspark26/frontend

# Files already in place:
# ✅ vite.config.js (configured for Vercel)
# ✅ package.json (React + Vite)
# ✅ .env.example (template for environment vars)
# ✅ VERCEL_DEPLOYMENT.md (detailed instructions)
# ✅ src/api/client.js (axios configured)
```

### 2.2 Create GitHub Repository

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit - RiskShield frontend"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/riskshield-frontend.git
git branch -M main
git push -u origin main
```

### 2.3 Deploy to Vercel

**Option A: Connect GitHub (Recommended)**
1. Go to [vercel.com](https://vercel.com)
2. Click "Import Project"
3. Choose "From Git" → Connect GitHub
4. Select `riskshield-frontend` repo
5. Click "Import"

**Option B: CLI**
```bash
npm install -g vercel
vercel login
vercel deploy
```

### 2.4 Add Environment Variables in Vercel

**Go to:** Project Settings → Environment Variables

Add:
```
VITE_API_URL=https://YOUR-USERNAME-riskshield-bfsi-x.hf.space
VITE_SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co
VITE_SUPABASE_ANON_KEY=YOUR-ANON-KEY
VITE_ENVIRONMENT=production
```

Save → Vercel auto-redeploys

### 2.5 Verify Frontend is Running

```
Frontend URL: https://riskshield-frontend.vercel.app
```

Open in browser → should load dashboard without errors

---

## Step 3: Test Full Integration — 5 min

### 3.1 Test Backend

```bash
# 1. Health check
curl https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/health

# 2. View API docs
# Go to: https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/docs
```

### 3.2 Test Frontend

```bash
# 1. Open frontend
# Go to: https://riskshield-frontend.vercel.app

# 2. Check browser console for errors
# Open DevTools: F12 → Console tab

# 3. Test API call
# Navigate to Alerts page → should fetch from backend
```

### 3.3 Test End-to-End

```bash
# From frontend:
1. Open Alerts page
2. Click "Refresh Alerts" button
3. Should show data from backend (even if empty)
4. No CORS errors = success!
```

---

## Deployment Checklist

### Backend (Hugging Face)
- [ ] Hugging Face Space created
- [ ] Code pushed to HF git
- [ ] All secrets added (SUPABASE_URL, DATABASE_URL, etc)
- [ ] Container built successfully (check Logs)
- [ ] `/api/health` returns 200
- [ ] Database connection confirmed

### Frontend (Vercel)
- [ ] GitHub repo created
- [ ] Code pushed to GitHub
- [ ] Vercel project imported
- [ ] Environment variables added (VITE_API_URL, etc)
- [ ] Build successful
- [ ] Frontend loads at vercel URL
- [ ] API calls work without CORS errors

### Integration
- [ ] Frontend can reach backend
- [ ] Backend can reach Supabase
- [ ] Data flows: Frontend → Vercel → Hugging Face → Supabase → back
- [ ] No 404, 500, or CORS errors

---

## Live URLs After Deployment

| Component | URL |
|-----------|-----|
| **Frontend** | https://riskshield-frontend.vercel.app |
| **Backend API** | https://YOUR-USERNAME-riskshield-bfsi-x.hf.space |
| **API Docs** | https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/docs |
| **Database** | postgresql://postgres:...@db.supabase.co:5432/postgres |

---

## Updating Deployments

### Update Backend Code

```bash
cd backend
# Make changes, test locally
git add .
git commit -m "Update: description of changes"
git push hf main
# Hugging Face auto-rebuilds (takes ~2-3 min)
```

### Update Frontend Code

```bash
cd frontend
# Make changes, test locally
npm run build
git add .
git commit -m "Update: description of changes"
git push origin main
# Vercel auto-deploys (takes ~1-2 min)
```

### Update Environment Variables

**Hugging Face:**
1. Go to Space → Settings → Secrets
2. Edit value, click Save
3. Space auto-restarts (~30 sec)

**Vercel:**
1. Go to Project Settings → Environment Variables
2. Edit value, click Save
3. Vercel auto-redeploys (~1-2 min)

---

## Monitoring & Debugging

### Check Backend Logs (Hugging Face)

1. Go to Space → **Logs** tab
2. Scroll to bottom to see real-time output
3. Look for errors like:
   - `Connection refused` → Database issue
   - `Module not found` → Missing dependency
   - `Port already in use` → Restart container

**Fix:** Update code/secrets, push again

### Check Frontend Logs (Vercel)

1. Go to Project → **Deployments**
2. Click latest deployment → **View build logs**
3. Look for:
   - `npm install` errors → missing package
   - `npm run build` errors → build issue
   - `Function duration` → build took too long

**Fix:** Add missing dependency, push to GitHub

### Check API Response (Browser DevTools)

1. Open frontend: https://riskshield-frontend.vercel.app
2. Press F12 → **Network** tab
3. Click API call (e.g., `/api/alerts`)
4. View **Response** tab
5. Should see JSON data, not HTML error

### Test API Directly

```bash
# Test health
curl -X GET "https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/health"

# Test alerts
curl -X GET "https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/alerts?limit=10"

# Test with auth
curl -X GET "https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/alerts" \
  -H "Authorization: Bearer YOUR-TOKEN"
```

---

## Troubleshooting

### "Connection refused" or "Cannot connect to database"

**Cause:** DATABASE_URL wrong or Supabase unreachable

**Fix:**
1. Copy exact connection string from Supabase
2. URL-encode special characters (e.g., `@` → `%40`)
3. Update in Hugging Face secrets
4. Restart container

### CORS Error: "Access to XMLHttpRequest blocked"

**Cause:** Backend CORS not allowing Vercel domain

**Fix:**
1. Update `backend/app.py` CORS middleware:
```python
allow_origins=["https://riskshield-frontend.vercel.app"]
```
2. Push backend code
3. Vercel frontend will work after HF rebuilds

### "ModuleNotFoundError: No module named 'xyz'"

**Cause:** Package not in `requirements.txt`

**Fix:**
1. Add to `backend/requirements.txt`
2. Push code
3. Hugging Face rebuilds with new packages

### Build takes >10 min

**Cause:** Large dependencies (catboost, sklearn) take time

**Normal for first build. Subsequent pushes are faster (cached layers)**

### Frontend shows "Cannot reach API"

**Cause:** VITE_API_URL wrong or backend down

**Fix:**
1. Check VITE_API_URL in Vercel env vars (no trailing slash)
2. Test backend URL directly: `curl https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/health`
3. If 404: backend not deployed yet

---

## Performance Tips

### Hugging Face Backend
- Keep requirements.txt minimal
- Use `slim` Python images (faster builds)
- Cache Docker layers (reuse base image)
- Use connection pooling (already done in database.py)

### Vercel Frontend
- Code splitting (Vite does auto)
- Lazy load components
- Optimize images
- Use production build: `npm run build`

---

## Security Best Practices

### Environment Variables
- ✅ Never commit `.env` to GitHub
- ✅ Use Vercel/Hugging Face secrets
- ✅ Rotate secrets regularly
- ✅ URL-encode special characters

### CORS
- ✅ Specify exact Vercel domain (not `*`)
- ✅ Whitelist only needed origins
- ✅ Use credentials flag for auth

### Database
- ✅ Use RLS policies (Row Level Security)
- ✅ Enable audit logging
- ✅ Regular backups via Supabase

---

## Next Steps After Deployment

1. **Record Demo Video**
   - Screen record: frontend + backend logs side-by-side
   - Show dashboard → alerts → graph view
   - Show API docs at `/docs`
   - Upload to YouTube (unlisted)

2. **Test with Real Data**
   - Run `python backend/data/seed_db.py` locally first
   - Then deploy seed script results to Supabase
   - Verify alerts appear in frontend

3. **Set Up Monitoring**
   - Hugging Face: Enable Space settings → auto-restart on crash
   - Vercel: Set up error alerts in Settings
   - Supabase: Enable email alerts for query slowness

4. **Document for Submission**
   - Add deployment URLs to README
   - Create architecture diagram
   - Write "How to Deploy" section
   - Screenshot dashboard, alerts, graph

---

**You're now live on Hugging Face + Vercel + Supabase!**
**Total deployment time: ~30 min**
**Estimated cost: $0 (all free tiers)**
