# RiskShield-BFSI-X — Complete Implementation Plan
### AI-Driven Correlation of Cybersecurity Telemetry & Transactional Behaviour (PS2)
### FinSpark'26 — Bank of Maharashtra

This plan takes you from an empty folder to a recordable, working demo. Every step is ordered so you can follow it top to bottom without re-planning mid-build. Time estimates assume you're working solo or with 1-2 teammates and reusing your existing RiskShield/Redrob/NERO code as described.

---

## 0. Before You Start — Decisions Locked In

- **Backend:** Python, FastAPI (same as RiskShield)
- **DB:** **PostgreSQL via Supabase** ✅ **NOW CONFIGURED** (fully managed, built-in auth, real-time subscriptions, REST API)
- **ML:** CatBoost (transaction stream, reused) + scikit-learn IsolationForest (security stream, reused pattern from Redrob)
- **Frontend:** React (Vite) + D3.js (reused NERO graph) + Recharts for KPI charts
- **Explanation layer:** Template-based first (like existing `hf_model.py`), optional Gemini API upgrade if time allows
- **Repo:** One monorepo, two folders: `backend/` and `frontend/`
- **Video tool:** OBS Studio or built-in screen recorder — plan the demo script now so you record clean footage once, not ten times

**Key Supabase Benefits for This Project:**
- ✅ PostgreSQL backend (same SQL/ORM compatibility — no code changes needed)
- ✅ Built-in Row Level Security (RLS) for RBAC (5-tier hierarchy: Analyst → CISO)
- ✅ Real-time listeners (optional, for live alert streaming via WebSocket)
- ✅ REST API (optional alternative to direct connection)
- ✅ Free tier includes 500 MB storage + unlimited API calls
- ✅ Automatic audit logging on all table changes (compliance-ready)
- ✅ Connection pooling built-in (no PgBouncer needed)

---

## ⚡ IMPORTANT: Supabase Setup Instructions

**You must complete these steps BEFORE building the application:**

### Step 1: Create Supabase Project (5 min)
1. Go to [supabase.com](https://supabase.com) → Click "New Project"
2. Enter project name: `riskshield-bfsi-x`
3. Set password (save this!)
4. Select region closest to India (Singapore preferred)
5. Wait ~2 minutes for project creation

### Step 2: Get Credentials (3 min)
1. Go to **Settings > Database > Connection strings**
2. Copy the **PostgreSQL connection string** (URI format)
3. Extract `PASSWORD` and `HOST` from the string
4. Also get your **API Key** from **Settings > API**

### Step 3: Fill `.env` File (2 min)
```bash
SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co
SUPABASE_KEY=eyJhbGci...YOUR-ANON-KEY...
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR-PROJECT-ID.supabase.co:5432/postgres
DATABASE_POOL_MAX=10
DATABASE_POOL_TIMEOUT=30
ENABLE_RLS=true
ENABLE_AUDIT_LOGGING=true
```

### Step 4: Initialize Database (2 min)
```bash
cd backend
python -c "from database import engine; from models import Base; Base.metadata.create_all(engine)"
```

### Step 5: Enable RLS & Audit Logging (optional but recommended for demo) (3 min)
1. Go to Supabase Dashboard → **SQL Editor**
2. Click **"New Query"**
3. Copy-paste from `backend/scripts/setup_rls.sql`
4. Click **"Run"**

**Total Setup Time: ~15 minutes**

See `SUPABASE_MIGRATION.md` for detailed migration guide and troubleshooting.

---

## 1. Folder Structure Setup

Create this exact structure first. Doing this before writing any code prevents mid-build reorganization.

```
riskshield-bfsi-x/
├── README.md
├── .gitignore
├── docker-compose.yml
├── backend/
│   ├── app.py                       # FastAPI entrypoint
│   ├── config.py
│   ├── database.py
│   ├── models.py                    # SQLAlchemy ORM models
│   ├── schemas.py                    # Pydantic request/response models
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── model/
│   │   └── catboost_fraud_model_balanced_tuned.cbm   # copy from RiskShield
│   ├── utils/
│   │   ├── auth.py                  # reuse from RiskShield
│   │   ├── tx_features.py           # transaction feature engineering (reused)
│   │   ├── security_features.py     # NEW: security telemetry feature engineering
│   │   ├── security_rules.py        # NEW: 5 deterministic security rules
│   │   ├── isolation_forest.py      # NEW: adapted from Redrob trap_detector.py
│   │   ├── correlation_engine.py    # NEW: the core PS2 differentiator
│   │   └── explain.py               # explanation generator (extended)
│   ├── data/
│   │   ├── generate_transactions.py # synthetic transaction generator
│   │   ├── generate_security_events.py # synthetic security telemetry generator
│   │   └── seed_db.py               # loads generated data into Postgres
│   └── tests/
│       └── test_client.py
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx        # KPI + charts (adapt RiskShield analytics page)
│   │   │   ├── Alerts.jsx           # correlated alerts table
│   │   │   └── GraphView.jsx        # D3 relationship graph (adapt from NERO)
│   │   ├── components/
│   │   │   ├── RiskBadge.jsx
│   │   │   ├── AlertCard.jsx
│   │   │   └── NetworkGraph.jsx     # ported NERO GraphViewer.jsx
│   │   └── api/
│   │       └── client.js
│   └── public/
└── docs/
    ├── architecture-diagram.png
    ├── demo-script.md
    └── screenshots/
```

**Action:**
```bash
mkdir -p riskshield-bfsi-x/{backend/{model,utils,data,tests},frontend/src/{pages,components,api},docs/screenshots}
cd riskshield-bfsi-x
git init
```

Copy your existing RiskShield files into `backend/` now (app.py, models.py, schemas.py, database.py, config.py, utils/auth.py, the .cbm model file, requirements.txt) so you're extending, not rewriting.

**Time: 20-30 min**

---

## 2. Environment Setup

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add Supabase-specific packages
pip install scikit-learn faker python-dotenv holidays catboost fastapi uvicorn sqlalchemy psycopg2-binary bcrypt supabase
```

### Frontend Setup
```bash
cd ../frontend
npm create vite@latest . -- --template react
npm install
npm install d3 recharts axios react-router-dom
```

### Update `.env` in `backend/` with Your Supabase Credentials

Copy `.env.example` and fill in:

```bash
# Get these from Supabase Dashboard
SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co
SUPABASE_KEY=eyJhbGci...YOUR-ANON-KEY...
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR-PROJECT-ID.supabase.co:5432/postgres

# Connection pooling (optimized for Supabase)
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=10
DATABASE_POOL_TIMEOUT=30

# Model and Engine Thresholds
FRAUD_THRESHOLD=0.6
SECURITY_TRAP_THRESHOLD=1.0
CORRELATION_WINDOW_SECONDS=900

# Authentication
SECRET_KEY=riskshield-bfsi-x-super-secret-key-change-me
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Feature Flags
ENABLE_RLS=true
ENABLE_AUDIT_LOGGING=true
ENABLE_REAL_TIME_ALERTS=true
```

### Verify Supabase Connection

```bash
# Test connection
python -c "from database import test_db_connection; print('✅ Connected!' if test_db_connection() else '❌ Failed!')"
```

**Time: 25-30 min** (including Supabase project creation — most of which is waiting for Supabase to spin up)

---

## 3. Database Schema — Supabase PostgreSQL (Extend, Don't Rebuild)

Keep your existing `users` and `predictions` tables untouched. Add two new tables with Supabase-optimized indexes.

### Key Changes for Supabase:
- ✅ All existing SQLAlchemy models work as-is (no code changes needed)
- ✅ Add indexes for RLS policies to work efficiently
- ✅ Audit logging is automatic (set up via `setup_rls.sql`)
- ✅ Connection pooling handled by `database.py` (includes `pool_pre_ping=True` for Supabase stability)

### Update `backend/models.py` — Add New Tables

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Index
from datetime import datetime
from database import Base

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(Integer, primary_key=True)
    customer_id = Column(String(50), nullable=False, index=True)
    email = Column(String(100), ForeignKey("users.email"), nullable=False)
    event_type = Column(String(30))               # login, failed_login, session_start
    device_fingerprint = Column(String(100))
    ip_address = Column(String(45))
    geo_location = Column(String(100))
    hard_flags = Column(JSON)
    iso_anomaly_flag = Column(Integer, default=0)
    security_trap_score = Column(Float, default=0.0)
    event_timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Optimize for Supabase RLS queries
    __table_args__ = (
        Index('idx_security_events_customer_timestamp', 'customer_id', 'event_timestamp'),
    )

class CorrelatedAlert(Base):
    __tablename__ = "correlated_alerts"
    id = Column(Integer, primary_key=True)
    customer_id = Column(String(50), index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"))
    security_event_id = Column(Integer, ForeignKey("security_events.id"))
    correlation_window_sec = Column(Integer)
    correlated_score = Column(Float)
    explanation = Column(String(500))  # Supabase free tier: optimize for string length
    risk_level = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Optimize for Supabase RLS queries
    __table_args__ = (
        Index('idx_correlated_alerts_customer', 'customer_id'),
        Index('idx_correlated_alerts_score_desc', 'correlated_score'),
        Index('idx_correlated_alerts_created_at_desc', 'created_at'),
    )
```

### Initialize Tables Automatically

Update `backend/app.py` to create tables on startup:

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db, dispose_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 RiskShield-BFSI-X starting...")
    init_db()  # Creates all tables if they don't exist
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("🔌 Shutting down...")
    dispose_db()  # Close connections gracefully

app = FastAPI(
    title="RiskShield-BFSI-X",
    description="AI-Driven Correlation of Cybersecurity Telemetry & Transactional Behaviour",
    version="1.0.0",
    lifespan=lifespan
)
```

### Optional: Enable RLS & Audit Logging

If you want to enable Row Level Security and automatic audit logging:

1. Go to Supabase Dashboard → **SQL Editor**
2. Copy-paste the entire `backend/scripts/setup_rls.sql` file
3. Click **"Run"**

This sets up:
- ✅ RLS policies for 5-tier RBAC (Branch Analyst → CISO)
- ✅ Automatic audit trail on all alert changes
- ✅ Analytics materialized view
- ✅ Performance indexes

**Time: 15-20 min** (database.py is already updated with connection pooling)

---

## 4. Synthetic Data Generation

You need two correlated synthetic datasets — not two unrelated random ones. The trick: some fraction of accounts should have a security event *and* a transaction close together in time, so your correlation engine has real positives to catch during the demo.

### 4.1 `backend/data/generate_transactions.py`

Reuse your RiskShield feature logic. Generate ~1,200 transactions across ~150 synthetic customers, ~7-8% fraud rate (matches your existing model's training distribution so scores stay meaningful).

```python
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("en_IN")

def generate_customers(n=150):
    return [{
        "customer_id": f"CUST{1000+i}",
        "email": fake.email(),
        "full_name": fake.name(),
        "kyc_verified": random.choice([1,1,1,0]),
        "account_age_days": random.randint(5, 2000),
    } for i in range(n)]

def generate_transaction(customer, force_fraud=False):
    amount = random.choice([
        random.uniform(500, 20000),          # normal
        random.uniform(80000, 300000)        # high-value (more likely if forcing fraud)
    ]) if not force_fraud else random.uniform(90000, 400000)
    hour = random.choice(range(6,22)) if not force_fraud else random.choice([0,1,2,3,23])
    dt = datetime.now() - timedelta(days=random.randint(0,30), hours=-hour)
    return {
        "customer_id": customer["customer_id"],
        "email": customer["email"],
        "transaction_id": fake.uuid4()[:12],
        "transaction_datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "transaction_amount": round(amount, 2),
        "kyc_verified": customer["kyc_verified"],
        "account_age_days": customer["account_age_days"],
        "channel_encoded": random.choice([0,1,2,3]),
    }
```

Generate ~1,200 rows, ~90-100 marked `force_fraud=True`.

### 4.2 `backend/data/generate_security_events.py`

For **each fraudulent transaction generated above**, also generate a correlated security event 2-14 minutes before it (this is what your correlation engine will catch). For the rest, generate normal/independent security events.

```python
SECURITY_EVENT_TYPES = ["login", "failed_login", "session_start"]
KNOWN_DEVICES = {}  # customer_id -> list of known device fingerprints

def generate_security_event(customer_id, email, correlated_to_txn_time=None, suspicious=False):
    if suspicious:
        device = fake.uuid4()[:16]              # never-seen device
        geo = random.choice(["Lagos, NG", "Manila, PH", "unknown proxy exit node"])
        failed_attempts = random.randint(3,6)
        event_time = correlated_to_txn_time - timedelta(minutes=random.randint(2,14))
    else:
        device = random.choice(KNOWN_DEVICES.get(customer_id, [fake.uuid4()[:16]]))
        geo = "Pune, IN"
        failed_attempts = 0
        event_time = fake.date_time_between(start_date="-30d", end_date="now")
    return {
        "customer_id": customer_id,
        "email": email,
        "event_type": "failed_login" if failed_attempts else "login",
        "device_fingerprint": device,
        "ip_address": fake.ipv4(),
        "geo_location": geo,
        "event_timestamp": event_time,
        "_failed_attempts_last_hour": failed_attempts,  # helper field for rule engine
    }
```

Generate:
- ~90 correlated suspicious pairs (matching the fraud transactions)
- ~400 additional independent/normal security events for realism (so the dashboard doesn't look suspiciously empty)

### 4.3 `backend/data/seed_db.py`

Loads both generated sets into Postgres, then runs each transaction through the existing `/api/predict` logic and each security event through the new rule engine (Section 5) to pre-populate `predictions`, `security_events`, and trigger `correlated_alerts` — so your dashboard has data the moment you boot the frontend.

```bash
python data/generate_transactions.py > data/transactions.json
python data/generate_security_events.py > data/security_events.json
python data/seed_db.py
```

**Time: 1.5-2 hours** (this is the highest-leverage step — good synthetic data makes the demo look credible)

---

## 5. Security Telemetry Engine (New — adapted from Redrob)

### 5.1 `backend/utils/security_rules.py` — Layer 1, deterministic

```python
def check_new_device(event, known_devices: set) -> bool:
    return event["device_fingerprint"] not in known_devices

def check_impossible_travel(event, last_event) -> bool:
    if not last_event:
        return False
    # simplified: different country + < 1 hour gap = impossible travel
    time_gap_hr = (event["event_timestamp"] - last_event["event_timestamp"]).total_seconds() / 3600
    return event["geo_location"].split(",")[-1].strip() != last_event["geo_location"].split(",")[-1].strip() and time_gap_hr < 1

def check_credential_stuffing(failed_attempts_last_hour: int) -> bool:
    return failed_attempts_last_hour >= 3

def check_off_hours_access(event) -> bool:
    hour = event["event_timestamp"].hour
    return hour in [0,1,2,3,4,23]

def check_session_anomaly(session_duration_sec: int, avg_duration_sec: float, std_duration_sec: float) -> bool:
    if std_duration_sec == 0:
        return False
    z = abs(session_duration_sec - avg_duration_sec) / std_duration_sec
    return z > 2.5

def run_all_rules(event, context) -> list:
    flags = []
    if check_new_device(event, context["known_devices"]):
        flags.append("new_device")
    if check_impossible_travel(event, context.get("last_event")):
        flags.append("impossible_travel")
    if check_credential_stuffing(event.get("_failed_attempts_last_hour", 0)):
        flags.append("credential_stuffing")
    if check_off_hours_access(event):
        flags.append("off_hours_access")
    if check_session_anomaly(context.get("session_duration",0), context.get("avg_duration",300), context.get("std_duration",60)):
        flags.append("session_anomaly")
    return flags
```

### 5.2 `backend/utils/isolation_forest.py` — Layer 2, statistical (ported from Redrob's `trap_detector.py`)

```python
from sklearn.ensemble import IsolationForest
import numpy as np

FEATURE_ORDER = [
    "failed_login_count_1h", "geo_velocity_kmh", "device_novelty_flag",
    "ip_reputation_score", "session_duration_zscore", "hour_of_day",
    "days_since_last_login", "login_frequency_deviation"
]

def build_feature_matrix(events_with_context: list) -> np.ndarray:
    return np.array([[e[f] for f in FEATURE_ORDER] for e in events_with_context])

def fit_and_flag(feature_matrix: np.ndarray, percentile=0.5):
    clf = IsolationForest(n_estimators=200, contamination="auto", random_state=42, n_jobs=-1)
    clf.fit(feature_matrix)
    raw_scores = clf.score_samples(feature_matrix)
    threshold = np.percentile(raw_scores, percentile)
    return (raw_scores < threshold).astype(int), clf
```

Same pattern as Redrob: `contamination="auto"`, manual percentile cutoff (use 0.5% instead of 0.3% since the security dataset is smaller — tune after first run).

### 5.3 Combine — `security_trap_score = len(hard_flags) + iso_flag`

Same tiering as Redrob: 0 = clean, 1 = soft flag, 2+ = hard flag.

**Time: 2-3 hours**

---

## 6. Correlation Engine (the core PS2 differentiator)

`backend/utils/correlation_engine.py`

```python
from datetime import timedelta

CORRELATION_WINDOW = timedelta(minutes=15)
CORRELATION_BONUS = 0.25

def find_correlated_pairs(security_events: list, transactions: list):
    """
    For each security event with trap_score >= 1, look for a transaction
    from the same customer_id within CORRELATION_WINDOW after it.
    """
    alerts = []
    for sec_event in security_events:
        if sec_event["security_trap_score"] < 1:
            continue
        for txn in transactions:
            if txn["customer_id"] != sec_event["customer_id"]:
                continue
            gap = txn["transaction_datetime"] - sec_event["event_timestamp"]
            if timedelta(0) <= gap <= CORRELATION_WINDOW and txn["combined_score"] >= 0.3:
                correlated_score = min(1.0, txn["combined_score"] + 
                                        (sec_event["security_trap_score"] / 3) + 
                                        CORRELATION_BONUS)
                alerts.append({
                    "customer_id": txn["customer_id"],
                    "prediction_id": txn["id"],
                    "security_event_id": sec_event["id"],
                    "correlation_window_sec": int(gap.total_seconds()),
                    "correlated_score": correlated_score,
                    "risk_level": score_to_level(correlated_score),
                })
    return alerts

def score_to_level(score):
    if score < 0.3: return "Low"
    if score < 0.6: return "Medium"
    if score < 0.8: return "High"
    return "Critical"
```

Run this as a scheduled job (every 30 sec via `asyncio` background task in FastAPI, or a manual `/api/run-correlation` endpoint you trigger for the demo).

**Time: 1.5-2 hours**

---

## 7. Explanation Layer

`backend/utils/explain.py` — extend your existing template generator:

```python
def generate_correlated_explanation(sec_event, txn, alert):
    return (
        f"⚠️ Flagged: {', '.join(sec_event['hard_flags'])} detected from "
        f"{sec_event['geo_location']} at {sec_event['event_timestamp'].strftime('%H:%M')}, "
        f"followed {alert['correlation_window_sec']//60} min later by a "
        f"₹{txn['transaction_amount']:,.0f} transfer "
        f"({', '.join(txn['rules_triggered'])}). "
        f"Correlated risk score: {alert['correlated_score']:.2f} — {alert['risk_level']}."
    )
```

If time allows, swap the f-string for a Gemini API call with the same inputs for a more natural-sounding explanation — but ship the template version first so you always have a working fallback.

**Time: 30-45 min (template) / +1 hr (Gemini upgrade, optional)**

---

## 8. API Endpoints to Build

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/predict` | POST | Existing — transaction scoring (reused) |
| `/api/security-event` | POST | NEW — ingest a security event, run rules + isolation forest |
| `/api/run-correlation` | POST | NEW — trigger correlation engine over recent window |
| `/api/alerts` | GET | NEW — list correlated alerts with explanations |
| `/api/alerts/{id}/graph` | GET | NEW — returns nodes/edges for D3 graph around one alert |
| `/api/analytics` | GET | Existing — extend with security + correlation KPIs |
| `/api/health` | GET | Existing |

**Time: 2 hours**

---

## 9. Frontend Build

Reuse RiskShield's dashboard shell and NERO's graph component — this is mostly wiring, not new design.

1. **Login page** — reuse RiskShield's existing login flow
2. **Dashboard** — KPI cards (total alerts, avg correlated score, top risk accounts) + Recharts trend line
3. **Alerts page** — table of `correlated_alerts`, sortable by risk_level, click row → expands explanation text
4. **GraphView page** — on clicking an alert, call `/api/alerts/{id}/graph`, render with ported `NetworkGraph.jsx` (relabel: node = account/device, edge = "logged in from" / "transferred to")

```bash
cd frontend
npm run dev
```

**Time: 3-4 hours**

---

## 10. Docker Compose (optional but strong for "ease of deployment" scoring criterion)

`docker-compose.yml`:
```yaml
version: "3.9"
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    env_file: ./backend/.env
  frontend:
    build: ./frontend
    ports: ["5173:5173"]
    depends_on: [backend]
```

**Time: 30 min**

---

## 11. Testing the Full Loop Before Recording

Run this checklist in order — every step must work before you record anything:

```bash
# 1. Seed data
python backend/data/seed_db.py

# 2. Start backend
uvicorn backend.app:app --reload --port 8000

# 3. Trigger correlation manually
curl -X POST http://localhost:8000/api/run-correlation

# 4. Confirm alerts exist
curl http://localhost:8000/api/alerts

# 5. Start frontend
cd frontend && npm run dev
```

Open `http://localhost:5173`, confirm:
- [ ] Dashboard loads with KPIs populated
- [ ] Alerts table shows at least 5-10 correlated alerts with readable explanations
- [ ] Clicking an alert opens the graph view with connected nodes
- [ ] Risk level colors render correctly (Low/Medium/High/Critical)

**Time: 30-45 min debugging buffer — budget this, something will break**

---

## 12. Demo Video Script (for recording)

Write this into `docs/demo-script.md` and rehearse once before recording for real.

**Structure (aim for 3-4 min total):**

1. **(0:00-0:20) Problem framing** — "Banks run security monitoring and fraud detection as two separate systems. A login anomaly and a suspicious transaction, each alone, often don't cross the alert threshold. Together, they're an account takeover. RiskShield-BFSI-X correlates both."
2. **(0:20-1:00) Show the dashboard** — KPIs, trend chart, mention it's built on a real fraud model (CatBoost, reused from a prior deployed system — credibility point).
3. **(1:00-2:00) Open the Alerts page** — click into one Critical alert, read the auto-generated explanation aloud, point out the specific security flag + transaction rule + time gap that triggered it.
4. **(2:00-2:45) Open the Graph view** for that alert — show the account, the new device, the beneficiary — "this is what a fraud analyst would investigate manually; we surface it automatically."
5. **(2:45-3:15) Briefly show the architecture diagram** (docs/architecture-diagram.png) — two streams, rule + ML hybrid on each, correlation engine, explanation layer, mention the post-quantum encryption note for the audit tables.
6. **(3:15-3:30) Close** — mention scalability (stateless FastAPI, works across branches) and that the core detection logic (rules + IsolationForest hybrid) is already proven in a separate deployed candidate-screening system you built, showing this isn't a one-off hack.

**Recording tips:**
- Record backend terminal + frontend browser in the same window (split screen or switch tabs) so the "real system running" feel comes through
- Do a dry run muted first to check timing
- Record in 1080p, keep browser zoom at 100%, close unrelated tabs/notifications

**Time: 45 min including 1 rehearsal + 1 real take**

---

## 13. Total Time Budget (rough)

| Phase | Time |
|---|---|
| Folder + env setup | 1 hr |
| DB schema | 40 min |
| Synthetic data generation | 2 hrs |
| Security rules + IsolationForest | 3 hrs |
| Correlation engine | 2 hrs |
| Explanation layer | 45 min |
| API endpoints | 2 hrs |
| Frontend wiring | 4 hrs |
| Docker compose | 30 min |
| Full-loop testing/debugging | 45 min |
| Demo script + recording | 45 min |
| **Total** | **~17-18 hrs** |

If you're tight on time, cut in this order: Docker compose first (nice-to-have), then Gemini explanation upgrade (template version is fine), then reduce synthetic dataset size (300 transactions instead of 1,200 still demos fine).

---

## 14. Submission Checklist (matches the FinSpark template)

- [ ] Prototype title + one-line description
- [ ] Problem statement selected + why
- [ ] Pre-requisites: Python 3.10+, Node 18+, PostgreSQL (Neon), CatBoost model file, Faker library
- [ ] Tools/resources list: FastAPI, CatBoost, scikit-learn, PostgreSQL, React, D3.js, Recharts, Docker
- [ ] Architecture diagram (export from draw.io or similar — two streams → correlation engine → explanation → dashboard)
- [ ] GitHub repo link (push everything, including `docs/demo-script.md`)
- [ ] Demo video link (upload to YouTube unlisted or Drive)
- [ ] Screenshots: dashboard, alert detail, graph view
- [ ] Key differentiators section: reused production-tested fraud model + trap-detection architecture from prior hackathon projects, explainability layer, temporal correlation logic, PQC-ready audit design

---

Ready to move to any specific section in more depth — the synthetic data generator, the correlation engine code, or the PPT/submission draft itself.