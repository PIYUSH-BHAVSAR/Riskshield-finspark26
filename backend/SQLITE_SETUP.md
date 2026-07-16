# RiskShield-BFSI-X — SQLite Local Setup (No External DB Needed)

## ✅ Your system is now configured to use SQLite (local database)

### What This Means:
- **No Supabase account needed** ✅
- **No PostgreSQL setup needed** ✅
- **Database stored locally** in `./riskshield.db` ✅
- **Works offline** ✅
- **Perfect for development & demo** ✅

---

## Quick Start (3 steps)

### Step 1: Install Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
python -c "from database import init_db; init_db()"
```

**Output should be:**
```
📊 Database: sqlite:///./riskshield.db
✅ SQLite database initialized (local)
📦 Creating database tables...
✅ Database tables initialized
```

### Step 3: Start Backend
```bash
uvicorn app:app --reload --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Test It Works

### In another terminal:
```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Should return:
# {"status":"healthy","service":"RiskShield-BFSI-X","database":"connected"}
```

### View API Docs:
```
http://localhost:8000/docs
```

---

## Database File

The SQLite database is stored in:
```
d:\projects\finspark26\riskshield.db
```

This is a single file that contains all tables:
- `users`
- `predictions`
- `security_events`
- `correlated_alerts`

---

## Seed Test Data

To populate with test data:
```bash
python backend/data/seed_db.py
```

Then check frontend to see alerts populated.

---

## Switching to Supabase Later (Optional)

If you want to switch to Supabase PostgreSQL later:

1. Update `.env`:
```
DATABASE_URL=postgresql://postgres:PASSWORD@db.supabase.co:5432/postgres
```

2. Restart backend — it auto-detects PostgreSQL and uses connection pooling

3. No code changes needed!

---

## Advantages of SQLite

✅ **Zero setup** — database is just a file
✅ **Fast** — optimized for local development
✅ **No server needed** — fully embedded
✅ **Works offline** — no internet required
✅ **Perfect for demo** — single command to restart clean

## Limitations of SQLite

⚠️ **Single-user** — not good for multi-user production
⚠️ **Limited concurrent writes** — but fine for demo
⚠️ **No real-time features** — no WebSocket subscriptions
⚠️ **No RLS/RBAC** — but not needed for demo

---

## Deployment Note

**For Hugging Face Spaces + Vercel deployment**, you have two options:

### Option 1: Keep SQLite (Simplest for Demo)
- ✅ Database included in Hugging Face container
- ✅ No external setup
- ✅ Works out of the box
- ⚠️ Data lost on container restart

### Option 2: Use Supabase (Production-Ready)
- ✅ Persistent data across restarts
- ✅ Professional audit logging
- ✅ Real-time features available
- ⚠️ Requires Supabase setup

---

## Your Current Setup

```
✅ Database: SQLite (./riskshield.db)
✅ Backend: FastAPI (http://localhost:8000)
✅ Frontend: React (http://localhost:5173)
✅ Ready to: Seed data → Deploy → Record demo video
```

---

**You're all set! Start backend and build the demo.** 🚀
