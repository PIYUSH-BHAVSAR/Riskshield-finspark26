# RiskShield-BFSI-X — Quick Deployment (30 min Total)

## TL;DR: 3 Simple Steps

### STEP 1: Deploy Backend to Hugging Face Spaces (10 min)

```bash
# 1. Create space at huggingface.co/spaces
# Name: riskshield-bfsi-x, Type: Docker

# 2. Push code
cd backend
git init
git remote add hf https://huggingface.co/spaces/YOUR-USERNAME/riskshield-bfsi-x
git add .
git commit -m "Deploy backend"
git push hf main

# 3. Add secrets in HF Space Settings:
SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co
SUPABASE_KEY=YOUR-ANON-KEY
DATABASE_URL=postgresql://postgres:Piyush%401665@db.ukoxjxfevchmfhctuqsa.supabase.co:5432/postgres
DATABASE_POOL_MAX=10
ENVIRONMENT=production
FRONTEND_URL=https://riskshield-frontend.vercel.app

# 4. Wait 2-3 min, then test:
curl https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/health
# Should return: {"status":"healthy",...}
```

**Backend URL:** `https://YOUR-USERNAME-riskshield-bfsi-x.hf.space` ✅

---

### STEP 2: Deploy Frontend to Vercel (10 min)

```bash
# 1. Push code to GitHub
cd frontend
git init
git remote add origin https://github.com/YOUR-USERNAME/riskshield-frontend
git add .
git commit -m "Deploy frontend"
git push -u origin main

# 2. Go to vercel.com → Import Project → Select GitHub repo

# 3. Add environment variables in Vercel:
VITE_API_URL=https://YOUR-USERNAME-riskshield-bfsi-x.hf.space
VITE_SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co
VITE_SUPABASE_ANON_KEY=YOUR-ANON-KEY

# 4. Save & Deploy (auto-deploys)
# Wait 1-2 min...
```

**Frontend URL:** `https://riskshield-frontend.vercel.app` ✅

---

### STEP 3: Verify Integration (5 min)

```bash
# 1. Test backend
curl https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/health

# 2. Open frontend
# https://riskshield-frontend.vercel.app

# 3. Check browser console (F12)
# Should see API calls going to HF backend, no CORS errors
```

---

## Files Already Ready for Deployment

**Backend:**
- ✅ `app.py` - FastAPI with all endpoints
- ✅ `database.py` - Supabase connection with pooling
- ✅ `requirements.txt` - All dependencies
- ✅ `Dockerfile` - Hugging Face compatible
- ✅ `HF_SPACES_README.md` - Detailed HF instructions

**Frontend:**
- ✅ `vite.config.js` - Vercel ready
- ✅ `package.json` - React + Vite configured
- ✅ `src/api/client.js` - Axios API client
- ✅ `.env.example` - Template for env vars
- ✅ `VERCEL_DEPLOYMENT.md` - Detailed Vercel instructions

**Database:**
- ✅ Supabase PostgreSQL (already configured)
- ✅ Connection string: `postgresql://postgres:Piyush%401665@db.ukoxjxfevchmfhctuqsa.supabase.co:5432/postgres`

---

## Deployment Architecture

```
Frontend (Vercel)
    ↓ axios calls (VITE_API_URL)
Backend (HF Spaces)
    ↓ psycopg2 connection
Database (Supabase)
```

---

## Getting Credentials

**From Supabase Dashboard:**
1. Settings → Database → Copy connection string
2. Settings → API → Copy anon key
3. Format connection string with URL-encoded password:
   ```
   postgresql://postgres:Piyush%401665@db.ukoxjxfevchmfhctuqsa.supabase.co:5432/postgres
   ```

**Paste into:**
- Hugging Face: Space Settings → Secrets
- Vercel: Project Settings → Environment Variables

---

## Test After Deployment

### Backend Health
```bash
curl https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/api/health
```
Expected: `{"status":"healthy",...}`

### API Documentation
```
https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/docs
```
(Swagger UI with all endpoints)

### Frontend Loading
```
https://riskshield-frontend.vercel.app
```
(Should load dashboard without errors)

### API Connectivity
Open frontend → F12 → Network tab → Make API call → Should see successful request to HF backend

---

## If Something Breaks

| Error | Cause | Fix |
|-------|-------|-----|
| Backend 500 error | DB connection failed | Check DATABASE_URL in HF secrets |
| CORS error on frontend | Backend missing Vercel domain | Update app.py CORS, push backend |
| Frontend can't load | VITE_API_URL wrong | Check Vercel env vars, redeploy |
| API returns 404 | Backend endpoint not implemented | Implement endpoint in app.py |
| Build takes forever | First build is slow (ML dependencies) | Normal, subsequent builds faster |

---

## Live URLs

| Service | URL |
|---------|-----|
| **Frontend** | https://riskshield-frontend.vercel.app |
| **Backend API** | https://YOUR-USERNAME-riskshield-bfsi-x.hf.space |
| **API Docs** | https://YOUR-USERNAME-riskshield-bfsi-x.hf.space/docs |
| **Database** | Supabase (behind backend) |

---

## Next: Record Demo Video

1. Open frontend + backend logs side-by-side
2. Show dashboard loading
3. Click Alerts → show list from backend
4. Click alert → show graph view
5. Show API docs at `/docs`
6. Upload to YouTube

**Time for video: ~5 min**

---

**You're live! 🚀**
**Total time: ~30 minutes**
**Total cost: $0 (free tiers)**
