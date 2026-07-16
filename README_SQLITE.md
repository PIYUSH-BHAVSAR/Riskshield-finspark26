# RiskShield-BFSI-X — SQLite Quick Start

## You're Using SQLite (Local Database) ✅

No Supabase needed. Database stored in `./riskshield.db`

---

## Start Backend (5 commands)

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -c "from database import init_db; init_db()"
uvicorn app:app --reload --port 8000
```

**Check it works:**
```bash
curl http://localhost:8000/api/health
```

Should return:
```json
{"status":"healthy","service":"RiskShield-BFSI-X","database":"connected"}
```

---

## Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Open: `http://localhost:5173`

---

## Seed Test Data

```bash
# In another terminal
cd backend
python data/seed_db.py
```

Then refresh frontend to see alerts populate.

---

## Check API Docs

```
http://localhost:8000/docs
```

Swagger UI with all endpoints

---

## Database File

Located at: `./riskshield.db`

Single SQLite file containing all tables:
- users
- predictions
- security_events
- correlated_alerts

---

## Deploy to Hugging Face + Vercel

### Backend (HF Spaces)
```bash
cd backend
git push hf main
# Update secrets in HF dashboard (DATABASE_URL=sqlite:///app/riskshield.db)
```

### Frontend (Vercel)
```bash
cd frontend
git push origin main
# Update VITE_API_URL in Vercel env vars
```

---

## Environment Variables

✅ **Already configured in `.env`:**
```
DATABASE_URL=sqlite:///./riskshield.db
FRAUD_THRESHOLD=0.6
SECURITY_TRAP_THRESHOLD=1.0
CORRELATION_WINDOW_SECONDS=900
SECRET_KEY=riskshield-bfsi-x-super-secret-key-change-me-in-production
```

No changes needed!

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `database locked` | Close other connections, restart backend |
| `table not found` | Run `python -c "from database import init_db; init_db()"` |
| `connection failed` | Check `.env` DATABASE_URL is correct |
| `CORS error` | Backend and frontend are on different ports (expected) |

---

## Files to Know

```
backend/
  ├── app.py              # FastAPI app (all endpoints)
  ├── database.py         # SQLite connection logic
  ├── models.py           # SQLAlchemy models
  ├── requirements.txt    # Python dependencies
  ├── .env               # Configuration (already set)
  ├── .env.example       # Template
  ├── data/
  │   └── seed_db.py    # Generate test data
  └── utils/
      ├── security_rules.py
      ├── isolation_forest.py
      ├── correlation_engine.py
      └── explain.py

frontend/
  ├── vite.config.js      # Build config
  ├── package.json        # Dependencies
  ├── src/
  │   ├── pages/         # Dashboard, Alerts, Graph
  │   ├── components/    # UI components
  │   └── api/
  │       └── client.js  # API calls
  └── .env.example       # Template
```

---

## API Endpoints Available

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Health check |
| POST | `/api/predict` | Score transaction |
| POST | `/api/security-event` | Ingest security event |
| POST | `/api/run-correlation` | Trigger correlation |
| GET | `/api/alerts` | List alerts |
| GET | `/api/alerts/{id}/graph` | Alert graph data |
| GET | `/api/analytics` | Dashboard KPIs |

---

## Next: Record Demo Video

1. Open frontend
2. Navigate to Alerts page
3. Click an alert
4. Show graph view
5. Show `/docs` endpoint
6. Record 3-5 min video

---

## Switch to Supabase Later?

1. Create Supabase account (optional)
2. Update `.env`: `DATABASE_URL=postgresql://...`
3. Restart backend
4. Done! No code changes needed

---

**Everything is ready. Start building!** 🚀
