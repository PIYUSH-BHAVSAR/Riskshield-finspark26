"""
RiskShield-BFSI-X - AI-Driven Fraud Detection & Security Telemetry Correlation
Backend API using FastAPI + Supabase PostgreSQL
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import database and models
from database import init_db, dispose_db, get_db, test_db_connection, SessionLocal
from models import Base

# ===== LIFESPAN CONTEXT MANAGER =====

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 RiskShield-BFSI-X starting...")
    try:
        if test_db_connection():
            logger.info("✅ Database connection successful")
            init_db()
            logger.info("✅ Database tables initialized")
        else:
            logger.error("❌ Database connection failed - some features may not work")
    except Exception as e:
        logger.error(f"⚠️ Database initialization warning: {e}")
    
    yield
    
    # Shutdown
    logger.info("🔌 Shutting down gracefully...")
    dispose_db()
    logger.info("✅ Resources cleaned up")

# ===== CREATE FASTAPI APP =====

app = FastAPI(
    title="RiskShield-BFSI-X",
    description="AI-Driven Correlation of Cybersecurity Telemetry & Transactional Behaviour",
    version="1.0.0",
    lifespan=lifespan
)

# ===== CORS MIDDLEWARE (allow Vercel frontend) =====

FRONTEND_URL = os.getenv("FRONTEND_URL", "*")  # "*" for Hugging Face Spaces testing, restrict in prod

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== HEALTH CHECK ENDPOINT =====

@app.get("/api/health", tags=["System"])
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint - confirms backend + database are running
    Used by: Vercel/monitoring, Hugging Face status checks
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "service": "RiskShield-BFSI-X",
            "version": "1.0.0",
            "database": "connected",
            "environment": os.getenv("ENVIRONMENT", "production")
        }
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e),
                "database": "disconnected"
            }
        )

# ===== PREDICTION ENDPOINTS (Transaction Fraud Detection) =====

@app.post("/api/predict", tags=["Fraud Detection"])
async def predict_fraud(
    transaction: dict,
    db: Session = Depends(get_db)
):
    """
    Score a transaction for fraud risk using CatBoost model + rules
    Input: transaction details
    Output: fraud_score (0-1), risk_level, explanation
    """
    try:
        # TODO: Implement with your existing RiskShield fraud model
        return {
            "transaction_id": transaction.get("transaction_id"),
            "fraud_score": 0.5,
            "risk_level": "Medium",
            "explanation": "Placeholder - connect to your CatBoost model"
        }
    except Exception as e:
        logger.error(f"❌ Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== SECURITY EVENT ENDPOINTS =====

@app.post("/api/security-event", tags=["Security Detection"])
async def ingest_security_event(
    event: dict,
    db: Session = Depends(get_db)
):
    """
    Ingest a security event (login, failed_login, session_start)
    Runs through deterministic rules + IsolationForest anomaly detection
    Output: security_trap_score, flags triggered
    """
    try:
        # TODO: Implement with security rules + isolation forest
        return {
            "event_id": event.get("event_id"),
            "security_trap_score": 0.0,
            "flags": [],
            "anomaly_detected": False
        }
    except Exception as e:
        logger.error(f"❌ Security event error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== CORRELATION ENDPOINTS =====

@app.post("/api/run-correlation", tags=["Correlation"])
async def trigger_correlation(db: Session = Depends(get_db)):
    """
    Trigger correlation engine to find linked security + fraud events
    Finds: security_event within 15 min of suspicious transaction for same customer
    Output: number of correlated alerts created
    """
    try:
        # TODO: Implement correlation engine
        return {
            "alerts_created": 0,
            "correlation_window_sec": 900,
            "status": "completed"
        }
    except Exception as e:
        logger.error(f"❌ Correlation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== ALERTS ENDPOINTS =====

@app.get("/api/alerts", tags=["Alerts"])
async def get_alerts(
    limit: int = 50,
    risk_level: str = None,
    db: Session = Depends(get_db)
):
    """
    Get correlated alerts (security + fraud combined)
    Supports filtering by risk_level: Low, Medium, High, Critical
    """
    try:
        # TODO: Query correlated_alerts table with explanations
        return {
            "alerts": [],
            "total": 0,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"❌ Alerts fetch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/alerts/{alert_id}/graph", tags=["Alerts"])
async def get_alert_graph(alert_id: int, db: Session = Depends(get_db)):
    """
    Get graph data for an alert (nodes + edges for D3 visualization)
    Nodes: account, device, beneficiary, IP
    Edges: login_from, transferred_to, shared_device
    """
    try:
        # TODO: Build graph around alert
        return {
            "nodes": [],
            "edges": [],
            "alert_id": alert_id
        }
    except Exception as e:
        logger.error(f"❌ Graph fetch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== ANALYTICS ENDPOINTS =====

@app.get("/api/analytics", tags=["Analytics"])
async def get_analytics(db: Session = Depends(get_db)):
    """
    Dashboard KPIs:
    - Total alerts, avg score, high-risk count
    - Trend data for charts
    - Top at-risk customers
    """
    try:
        # TODO: Query materialized views or aggregates
        return {
            "total_alerts": 0,
            "avg_correlated_score": 0.0,
            "critical_alerts": 0,
            "alerts_by_hour": [],
            "top_risk_customers": []
        }
    except Exception as e:
        logger.error(f"❌ Analytics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== SEED DATA ENDPOINT (for testing) =====

@app.post("/api/seed-data", tags=["Testing"])
async def seed_test_data(db: Session = Depends(get_db)):
    """
    Populate test data (transactions + security events) for demo
    WARNING: Only enable in development
    """
    if os.getenv("ENVIRONMENT") == "production":
        raise HTTPException(status_code=403, detail="Seeding disabled in production")
    
    try:
        # TODO: Call data generation functions
        return {
            "transactions_created": 0,
            "security_events_created": 0,
            "alerts_created": 0
        }
    except Exception as e:
        logger.error(f"❌ Seeding error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== ERROR HANDLERS =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status": "error"
        }
    )

# ===== ROOT ENDPOINT =====

@app.get("/", tags=["Info"])
async def root():
    """API info endpoint"""
    return {
        "name": "RiskShield-BFSI-X",
        "version": "1.0.0",
        "description": "AI-Driven Correlation of Cybersecurity Telemetry & Transactional Behaviour",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

# ===== FOR LOCAL TESTING =====

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
