# RiskShield-BFSI-X → Supabase Migration Guide

## Overview
This document details all changes made to switch from PostgreSQL/Neon to **Supabase** as the database provider.

## Why Supabase for This Project?

| Feature | Benefit |
|---------|---------|
| **PostgreSQL-Compatible** | SQLAlchemy, psycopg2, and all existing ORM code works without changes |
| **Row Level Security (RLS)** | Built-in RBAC perfect for banking — Branch Analyst, Fraud Analyst, CISO tiers |
| **Real-time Subscriptions** | Optional live alert streaming to frontend (WebSocket) |
| **REST API** | Auto-generated endpoint for each table — optional alternative to direct connection |
| **Free Tier** | 500 MB storage + unlimited API calls — enough for demo |
| **Authentication** | Built-in JWT auth (optional — use your own for this project) |
| **Audit Logging** | Built-in `audit` schema tracks all changes to tables |

---

## Changes Made to the Codebase

### 1. **Environment Variables** (`.env.example`)

**Changed:**
- ✅ Added `SUPABASE_URL` — REST endpoint (optional)
- ✅ Added `SUPABASE_KEY` — anon/service key
- ✅ Updated `DATABASE_URL` — now points to Supabase PostgreSQL URL format
- ✅ Added connection pooling params (`DATABASE_POOL_MIN`, `DATABASE_POOL_MAX`, `DATABASE_POOL_TIMEOUT`)
- ✅ Added feature flags (`ENABLE_REAL_TIME_ALERTS`, `ENABLE_AUDIT_LOGGING`, `ENABLE_RLS`)

**Your .env file will now look like:**
```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGci...your-anon-key...
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.your-project-id.supabase.co:5432/postgres
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=10
FRAUD_THRESHOLD=0.6
SECURITY_TRAP_THRESHOLD=1.0
CORRELATION_WINDOW_SECONDS=900
SECRET_KEY=your-secret-here
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENABLE_REAL_TIME_ALERTS=true
ENABLE_AUDIT_LOGGING=true
ENABLE_RLS=true
```

### 2. **Database Connection** (`backend/database.py`)

**Before:**
```python
from sqlalchemy import create_engine
engine = create_engine(os.getenv("DATABASE_URL"))
```

**After (with connection pooling):**
```python
from sqlalchemy import create_engine, event
from sqlalchemy.pool import QueuePool
import os

database_url = os.getenv("DATABASE_URL")

# Supabase requires connection pooling for reliable connections
engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=int(os.getenv("DATABASE_POOL_MAX", 10)),
    max_overflow=5,
    pool_pre_ping=True,  # Test connection before using (Supabase stability)
    connect_args={"connect_timeout": 10}
)

# Optional: Add event listener for better error handling
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("SET timezone = 'UTC'")
    cursor.close()
```

### 3. **Database Models** (`backend/models.py`)

**No changes to model definitions** — they work as-is. But add index hints for Supabase Row Level Security:

```python
# In your SecurityEvent model, add:
__table_args__ = (
    Index('idx_security_events_customer_email', 'customer_id', 'email'),
    Index('idx_security_events_timestamp', 'event_timestamp'),
)

# In your CorrelatedAlert model, add:
__table_args__ = (
    Index('idx_correlated_alerts_customer', 'customer_id'),
    Index('idx_correlated_alerts_score', 'correlated_score'),
)
```

This improves query performance for the RLS policies.

### 4. **Initialize Database on Startup** (`backend/app.py`)

**Add this to FastAPI startup:**

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine
from models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("📦 Creating tables if they don't exist...")
    Base.metadata.create_all(engine)
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("🔌 Closing database connections...")
    engine.dispose()

app = FastAPI(lifespan=lifespan)
```

This ensures tables are created on first run without manual migration commands.

### 5. **Optional: Supabase Real-time Listener** (`backend/utils/realtime.py`)

**NEW FILE** — For live alert streaming (optional):

```python
import os
import json
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Optional: Use for real-time alerts on frontend
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def subscribe_to_alerts(customer_id: str, callback):
    """Listen for new alerts for a specific customer in real-time."""
    
    def handle_change(payload):
        if payload["eventType"] == "INSERT":
            alert = payload["new"]
            callback(alert)
    
    supabase.realtime.on(
        "correlated_alerts",
        "*",
        handle_change
    ).subscribe()
```

**Frontend usage** (optional):
```javascript
// In frontend/src/api/client.js
const { data, status } = supabase
  .from('correlated_alerts')
  .on('*', payload => {
    console.log('New alert:', payload.new);
    setAlerts(prev => [...prev, payload.new]);
  })
  .subscribe();
```

### 6. **Row Level Security (RLS) Setup** (`backend/scripts/setup_rls.sql`)

**NEW FILE** — Run this SQL in Supabase dashboard > SQL Editor:

```sql
-- ===== ENABLE RLS ON ALL TABLES =====

ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.security_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.correlated_alerts ENABLE ROW LEVEL SECURITY;

-- ===== CREATE ROLE-BASED POLICIES =====

-- Branch Analyst: can see only their own customer records
CREATE POLICY branch_analyst_view_alerts
  ON correlated_alerts
  FOR SELECT
  USING (auth.uid() = customer_id OR 
         (SELECT role FROM users WHERE email = auth.email()) = 'branch_analyst');

-- Fraud Analyst: can see all alerts, add notes
CREATE POLICY fraud_analyst_manage_alerts
  ON correlated_alerts
  FOR SELECT
  USING ((SELECT role FROM users WHERE email = auth.email()) IN ('fraud_analyst', 'fraud_lead', 'security_ops', 'ciso'));

CREATE POLICY fraud_analyst_update_alerts
  ON correlated_alerts
  FOR UPDATE
  USING ((SELECT role FROM users WHERE email = auth.email()) IN ('fraud_analyst', 'fraud_lead', 'security_ops', 'ciso'))
  WITH CHECK ((SELECT role FROM users WHERE email = auth.email()) IN ('fraud_analyst', 'fraud_lead', 'security_ops', 'ciso'));

-- CISO: unrestricted access
CREATE POLICY ciso_unrestricted
  ON correlated_alerts
  FOR ALL
  USING ((SELECT role FROM users WHERE email = auth.email()) = 'ciso');

-- Deny direct customer_id updates (immutable once created)
CREATE POLICY prevent_customer_id_change
  ON correlated_alerts
  FOR UPDATE
  USING (TRUE)
  WITH CHECK (customer_id = (SELECT customer_id FROM correlated_alerts WHERE id = correlated_alerts.id));

-- ===== AUDIT LOGGING =====

-- Create audit table (optional, Supabase does this automatically)
CREATE TABLE IF NOT EXISTS audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name TEXT,
    record_id INTEGER,
    action TEXT,
    old_data JSONB,
    new_data JSONB,
    changed_by TEXT,
    changed_at TIMESTAMP DEFAULT NOW()
);

-- Optional: Auto-log all correlated_alert changes
CREATE OR REPLACE FUNCTION audit_correlated_alerts()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, changed_by, changed_at)
    VALUES (
        'correlated_alerts',
        COALESCE(NEW.id, OLD.id),
        TG_OP,
        to_jsonb(OLD),
        to_jsonb(NEW),
        CURRENT_USER,
        NOW()
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_audit_correlated_alerts
AFTER INSERT OR UPDATE OR DELETE ON correlated_alerts
FOR EACH ROW
EXECUTE FUNCTION audit_correlated_alerts();
```

### 7. **Connection Pooling Middleware** (`backend/middleware/db.py`)

**NEW FILE** — For better connection reuse:

```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from database import engine

class DatabaseConnectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Pre-ping connection to avoid stale connections with Supabase
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        response = await call_next(request)
        return response

# Add to app:
# app.add_middleware(DatabaseConnectionMiddleware)
```

### 8. **Requirements.txt Updates**

**Add these packages:**

```
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0  # PostgreSQL adapter (works with Supabase)
supabase>=2.3.0         # Optional: for real-time and admin API
python-jose[cryptography]>=3.3.0
python-dotenv>=1.0.0
```

---

## How to Set Up Supabase (Step-by-Step)

### Step 1: Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Click "New Project"
3. Enter:
   - **Project name:** `riskshield-bfsi-x`
   - **Password:** Copy this — it's your `[PASSWORD]`
   - **Region:** Closest to India (e.g., Singapore)
4. Click "Create new project" — wait ~2 min

### Step 2: Get Connection Credentials
1. Once project is ready, go to **Settings > Database**
2. Copy the **"Connection string"** (URI format)
3. Format: `postgresql://postgres:PASSWORD@HOST:5432/postgres`
4. Extract:
   - `PASSWORD` → use as `[PASSWORD]` in URLs
   - `HOST` → your Supabase hostname (e.g., `db.xxx.supabase.co`)

### Step 3: Fill Your `.env` File
```bash
SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co
SUPABASE_KEY=YOUR-ANON-KEY  # from Settings > API
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR-PROJECT-ID.supabase.co:5432/postgres
```

### Step 4: Initialize Database
```bash
cd backend
python -c "from database import engine; from models import Base; Base.metadata.create_all(engine)"
```

### Step 5: (Optional) Enable RLS
1. In Supabase dashboard, go to **SQL Editor**
2. Click **"New Query"**
3. Paste the SQL from `backend/scripts/setup_rls.sql`
4. Click **"Run"**

---

## Key Differences from Neon PostgreSQL

| Aspect | Neon | Supabase |
|--------|------|---------|
| **Connection String** | Standard PostgreSQL | Standard PostgreSQL (same format) |
| **Connection Pooling** | Via PgBouncer (external) | Built-in via Supabase Realtime |
| **RLS Support** | ✅ Yes, manual setup | ✅ Yes, easier dashboard UI |
| **Real-time** | ✗ No | ✅ Yes (WebSocket-based) |
| **REST API** | ✗ No | ✅ Auto-generated |
| **Storage** | Free tier: 3 GB | Free tier: 500 MB (fine for demo) |
| **Auth** | Manual JWT | Built-in (optional) |
| **Audit Logging** | Manual | Built-in `audit` schema |

---

## Debugging Supabase Connection Issues

### Error: "Connection timeout"
**Cause:** Supabase requires `pool_pre_ping=True`
**Fix:** Ensure `database.py` has this setting (already added above)

### Error: "Role postgres does not exist"
**Cause:** Wrong password or hostname
**Fix:** Double-check credentials in Supabase > Settings > Database

### Error: "SSL certificate verify failed"
**Cause:** Supabase uses SSL by default
**Fix:** Add to connection string: `?sslmode=require`

```python
database_url = os.getenv("DATABASE_URL")
if "supabase" in database_url:
    database_url += "?sslmode=require"
```

### Alert: "Idle connections closed after 10 min"
**Cause:** Supabase closes idle connections
**Fix:** Set `pool_recycle=300` (recycle every 5 min)

```python
engine = create_engine(
    database_url,
    pool_recycle=300,  # Add this
    ...
)
```

---

## Real-time Alerts Feature (Optional)

If `ENABLE_REAL_TIME_ALERTS=true`, the frontend will listen to Supabase real-time and update the alerts table without page refresh:

```javascript
// frontend/src/hooks/useRealtimeAlerts.js
import { supabase } from '../api/supabaseClient';
import { useEffect, useState } from 'react';

export function useRealtimeAlerts(customerId) {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const subscription = supabase
      .from(`correlated_alerts:customer_id=eq.${customerId}`)
      .on('*', payload => {
        setAlerts(prev => [...prev, payload.new]);
      })
      .subscribe();

    return () => subscription.unsubscribe();
  }, [customerId]);

  return alerts;
}
```

---

## Performance Tips for Supabase

1. **Use indexes** — Already added in models (see Section 3)
2. **Enable RLS** — Slows queries by ~5% but critical for security (worth it)
3. **Batch inserts** — Use bulk insert for synthetic data (~500 records per batch)
4. **Paginate queries** — Always add `LIMIT 100` to list endpoints
5. **Cache frequently-read data** — e.g., customer baseline stats (use Redis if available)

---

## Checklist Before Going Live

- [ ] `.env` file filled with Supabase credentials
- [ ] `backend/database.py` updated with pooling config
- [ ] `backend/app.py` has lifespan function for table creation
- [ ] Ran `setup_rls.sql` in Supabase SQL Editor (if using RLS)
- [ ] Tested `/api/health` endpoint — should return 200
- [ ] Ran `seed_db.py` — should populate `security_events` and `predictions`
- [ ] Frontend `/api/alerts` shows populated data
- [ ] Demo runs without "Connection lost" errors

---

## Support & Resources

- **Supabase Docs:** https://supabase.com/docs
- **SQLAlchemy Supabase:** https://supabase.com/docs/guides/getting-started/quickstarts/build-a-python-app
- **Real-time Docs:** https://supabase.com/docs/guides/realtime/quickstart
- **RLS Guide:** https://supabase.com/docs/learn/auth-deep-dive/row-level-security
