# RiskShield-BFSI-X 🛡️
### AI-Driven Correlation of Cybersecurity Telemetry & Transactional Behaviour
**Bank of Maharashtra Cyber Security Hackathon (FinSpark '26) — Problem Statement 2**

---

## 📌 Executive Summary
**RiskShield-BFSI-X** is an enterprise-grade, real-time threat intelligence and fraud prevention platform built for the modern banking ecosystem. 

Traditional banking security systems monitor transactional fraud and network security in siloed dashboards. RiskShield-BFSI-X bridges this gap. By combining machine learning (CatBoost) for transactional fraud detection and unsupervised learning (Isolation Forest) for security telemetry anomaly detection, it runs a **temporal correlation engine** with a 15-minute sliding window. This catches advanced fraud vectors—such as Credential Stuffing followed by High-Value transfers—that either engine alone would fail to flag.

---

## 🚀 Key Features

*   **Dual-Engine Analytics**:
    *   **CatBoost Classifier**: Analyzes transactional patterns (amount, velocity, age, hour) trained on historical behavioral distributions.
    *   **Isolation Forest**: Detects statistical outliers in security log metadata (device logins, geography shifts, failed attempts).
*   **Temporal Correlation Engine**: Performs sliding-window time matches across both transaction and security streams, applying a decay/bonus weight based on event timing gap.
*   **Auto-Generated Threat Narratives**: Translates complex ML outputs and rule triggers into structured plain-English audit trails for fraud analysts.
*   **D3.js Force-Directed Graph**: Visually links customers, compromised devices, geolocation alerts, and fraudulent transfers to expose systemic attacks.
*   **PQC Auditing Vision**: Incorporates a design pathway for securing stored audit logs against "Harvest Now, Decrypt Later" threat vectors using NIST-approved post-quantum algorithms.

---

## 📐 Architecture & Data Flow

```
                     ┌──────────────────┐
                     │ Transaction Data │
                     └────────┬─────────┘
                              ▼
                  ┌──────────────────────┐
                  │ Feature Engineering  │
                  └────────┬─────────────┘
                              ▼
                  ┌──────────────────────┐
                  │   CatBoost Engine    ├────────┐
                  └──────────────────────┘        │
                                                  ▼
                                      ┌───────────────────────┐
                                      │  Correlation Engine   │
                                      │ (15-min Time Window)  │
                                      └───────────┬───────────┘
                                                  ▼
                                      ┌───────────────────────┐
                                      │  Explanation Engine   │
                                      └───────────┬───────────┘
                                                  ▼
                                      ┌───────────────────────┐
                                      │  Analyst Dashboard    │
                                      │ (React + Recharts/D3) │
                                      └───────────────────────┘
                                                  ▲
                                      ┌───────────┴───────────┐
                                      │ Security Anomaly Det. │
                                      └───────────────────────┘
                                                  ▲
                  ┌──────────────────────┐        │
                  │  Isolation Forest    ├────────┘
                  └──────────▲───────────┘
                             │
                  ┌──────────┴───────────┐
                  │  Security Telemetry  │
                  └──────────────────────┘
```

---

## 🛠️ Tech Stack

*   **Backend API**: FastAPI (Python 3.10+), SQLAlchemy Core, Uvicorn, Pydantic v2
*   **Machine Learning**: CatBoost Classifier, scikit-learn (Isolation Forest), Pandas, NumPy
*   **Database**: PostgreSQL (managed via Supabase connection pooling) / SQLite local fallback
*   **Frontend**: React (Vite), D3.js (Force-Directed Graph), Recharts (KPI Trends), Tailwind CSS / Vanilla variables
*   **Infrastructure**: Docker, dotenv, bcrypt (native encryption)

---

## 📁 Repository Structure

```
finspark26/
├── backend/                     # Python Backend
│   ├── app.py                   # REST API routes (Ingestion, Alerts, Analytics)
│   ├── database.py              # Connection pooling & ORM engine
│   ├── models.py                # User, Transaction, SecurityEvent, CorrelatedAlert tables
│   ├── schemas.py               # Pydantic validation models
│   ├── utils/
│   │   ├── auth.py              # JWT authentication & bcrypt security
│   │   ├── tx_features.py       # ML feature extraction pipeline
│   │   ├── security_rules.py    # Deterministic heuristics parser
│   │   ├── isolation_forest.py  # Anomaly detection model wrapper
│   │   ├── correlation_engine.py # Temporal mapping & risk scoring
│   │   └── explain.py           # Auto-generated textual risk breakdown
│   ├── data/
│   │   ├── generate_data.py     # Multi-tier synthetic generator
│   │   └── seed_db.py           # DB seeder & model training trigger
│   ├── model/                   # Serialized ML model binaries (.cbm, .pkl)
│   └── tests/
│       └── test_client.py       # End-to-end API integration tests
└── frontend/                    # React Frontend
    └── src/
        ├── api/client.js        # Axios instance + JWT interceptors
        ├── components/
        │   ├── RiskBadge.jsx    # Alert level classification color pill
        │   └── NetworkGraph.jsx # Interactive D3.js visual network
        └── pages/
            ├── Login.jsx        # Analyst Authentication Portal
            ├── Dashboard.jsx    # Real-time Operations Center & Trends
            └── Alerts.jsx       # Alert Inbox & Deep-dive Inspector Panel
```

---

## 🧮 Score & Escalation Formula

The correlation risk engine blends transaction threat levels and security metrics using parameters optimized through grid search to eliminate alert fatigue:

$$\text{Correlated Score} = \min\left(1.0, 0.15 + (S_{\text{transaction}} \times 0.25) + (S_{\text{security\_trap}} \times 0.05) + \text{Time Bonus}\right)$$

### 🕒 Time-Based Correlation Bonus:
*   Gap $\le 5\text{ mins}$: $+0.20$
*   Gap $\le 10\text{ mins}$: $+0.12$
*   Gap $\le 15\text{ mins}$: $+0.05$

### 🚦 Threat Classification:
*   **Low** ($\text{Score} < 0.30$)
*   **Medium** ($0.30 \le \text{Score} < 0.65$)
*   **High** ($0.65 \le \text{Score} < 0.80$)
*   **Critical** ($\text{Score} \ge 0.80$)

---

## ⚙️ Local Installation & Running Guide

### Prerequisites
Make sure you have **Python 3.10+** and **Node.js 18+** installed.

### 1. Setup Backend environment
```bash
# Navigate to project root
cd D:/projects/finspark26

# Create virtual environment and activate
python -m venv backend/venv
# Windows:
.\backend\venv\Scripts\activate

# Install python dependencies
pip install -r backend/requirements.txt
```

### 2. Configure Environment variables
Create/verify the `.env` file at `backend/.env` with these parameters:
```env
DATABASE_URL=sqlite:///D:/projects/finspark26/riskshield.db
FRAUD_THRESHOLD=0.6
SECURITY_TRAP_THRESHOLD=1.0
CORRELATION_WINDOW_SECONDS=900
SECRET_KEY=riskshield-bfsi-x-super-secret-key-change-me-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENABLE_REAL_TIME_ALERTS=true
ENABLE_AUDIT_LOGGING=true
```

### 3. Generate Datasets & Train Models
Execute the database initialization, seeding, and ML pipeline training script:
```bash
$env:PYTHONPATH = "D:\projects\finspark26"
python backend/data/seed_db.py
```
*This will drop/create tables, synthesize a multi-tiered data set, train the CatBoost classifier and Isolation Forest anomaly models, run correlation matching, and write initial records.*

### 4. Run API Server
Start the Uvicorn web gateway:
```bash
$env:PYTHONPATH = "D:\projects\finspark26"
python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```
*   **Swagger Docs**: Available at `http://localhost:8000/docs`
*   **JSON OpenAPI**: Available at `http://localhost:8000/openapi.json`

### 5. Setup & Launch UI Client
Open a second terminal window:
```bash
cd D:/projects/finspark26/frontend
npm install
npm run dev
```
*   **Web Console URL**: Open `http://localhost:5173`
*   **Demo Login Credentials**: 
    *   **Email**: `admin@riskshield.com`
    *   **Password**: `admin123`

---

## 🧪 Verification & Testing
To ensure the backend API behaves correctly, run the pre-built test suite:
```bash
$env:PYTHONPATH = "D:\projects\finspark26"
python backend/tests/test_client.py
```
**Expected Console Output:**
```text
==================================================
  RISKSHIELD-BFSI-X API INTEGRATION TESTS
==================================================
Testing /api/analytics endpoint...
[PASS] Analytics endpoint verified successfully.
       Dashboard Stats: Total Alerts=26, Critical=8, Risk Avg=62.0%
Testing /api/auth/login endpoint...
[PASS] Authentication endpoint verified successfully.
Testing /api/alerts & graph endpoints...
[PASS] Alert list endpoint verified. Found 26 alerts.
[PASS] Alert D3 Graph data endpoint verified successfully.
       Alert #AL-1 Network: Nodes=6, Links=6
Testing /api/transactions endpoint...
[PASS] Transactions endpoint verified. Found 50 transactions.

==================================================
  ALL BACKEND API TESTS PASSED!
==================================================
```

---

## 🔒 Post-Quantum Cryptography & Auditability
In banking environments, audit logs and telemetry data must remain confidential and untampered for several decades. Traditional RSA and ECC encryptions are vulnerable to "Harvest Now, Decrypt Later" schemes. 

RiskShield-BFSI-X incorporates a design pathway to wrap archived correlation logs using **PQC (Post-Quantum Cryptography)** standards. By applying **ML-KEM (Kyber)** for key encapsulation and **ML-DSA (Dilithium)** for code signatures, we ensure that compliance logs remain fully authenticated and safe from future quantum decryption attacks.
