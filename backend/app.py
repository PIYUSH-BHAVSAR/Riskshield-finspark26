"""
RiskShield-BFSI-X - AI-Driven Fraud Detection & Security Telemetry Correlation
Backend API using FastAPI + Supabase PostgreSQL
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Form
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

# ===== AUTHENTICATION ENDPOINTS =====

@app.post("/api/auth/login", tags=["Authentication"])
async def login(username: str = Form(...), password: str = Form(...)):
    """
    Simple login endpoint - accepts username/password in form data
    Returns JWT token for authenticated requests
    Default credentials: admin@riskshield.com / admin123
    """
    # Simple hardcoded auth for demo (replace with database lookup in production)
    if username == "admin@riskshield.com" and password == "admin123":
        return {
            "access_token": "demo-token-riskshield-bfsi-x",
            "token_type": "bearer",
            "user": {
                "email": "admin@riskshield.com",
                "role": "analyst"
            }
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
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
    from models import CorrelatedAlert
    
    try:
        query = db.query(CorrelatedAlert)
        
        # Filter by risk level if provided
        if risk_level and risk_level != "All":
            query = query.filter(CorrelatedAlert.risk_level == risk_level)
        
        # Get total and limited results
        total = query.count()
        alerts_data = query.order_by(CorrelatedAlert.created_at.desc()).limit(limit).all()
        
        # Format for frontend
        alerts_list = [
            {
                "id": a.id,
                "customer_id": a.customer_id,
                "transaction_id": a.transaction_id,
                "security_event_id": a.security_event_id,
                "correlated_score": round(a.correlated_score, 2),
                "risk_level": a.risk_level,
                "explanation": a.explanation,
                "status": a.status,
                "created_at": a.created_at.isoformat() if a.created_at else None
            }
            for a in alerts_data
        ]
        
        return {
            "alerts": alerts_list,
            "total": total,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"❌ Alerts fetch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/alerts/{alert_id}", tags=["Alerts"])
async def update_alert_status(alert_id: int, body: dict, db: Session = Depends(get_db)):
    """
    Update alert status (open, investigating, resolved, false_positive)
    """
    from models import CorrelatedAlert
    from pydantic import BaseModel
    
    class AlertUpdate(BaseModel):
        status_update: str
    
    try:
        # Parse the body
        status_update = body.get("status_update") if isinstance(body, dict) else None
        
        if not status_update:
            raise HTTPException(status_code=400, detail="status_update required")
        
        alert = db.query(CorrelatedAlert).filter(CorrelatedAlert.id == alert_id).first()
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        valid_statuses = ["open", "investigating", "resolved", "false_positive"]
        if status_update not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        
        alert.status = status_update
        db.commit()
        
        return {
            "id": alert.id,
            "status": alert.status,
            "message": "Alert status updated"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Alert update error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/alerts/{alert_id}/graph", tags=["Alerts"])
async def get_alert_graph(alert_id: int, db: Session = Depends(get_db)):
    """
    Get graph data for an alert (nodes + edges for D3 visualization)
    Nodes: customer, transaction, security_event, device, IP
    Edges: login_from, transferred_to, shared_device
    """
    from models import CorrelatedAlert, Transaction, SecurityEvent
    
    try:
        alert = db.query(CorrelatedAlert).filter(CorrelatedAlert.id == alert_id).first()
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        nodes = []
        edges = []
        
        # Node 1: Customer (always present)
        nodes.append({
            "id": f"cust_{alert.customer_id}",
            "label": alert.customer_id,
            "type": "customer",
            "value": 30
        })
        
        # Node 2: Transaction + edges
        if alert.transaction_id:
            txn = db.query(Transaction).filter(Transaction.id == alert.transaction_id).first()
            if txn:
                nodes.append({
                    "id": f"tx_{txn.id}",
                    "label": txn.transaction_id,
                    "type": "transaction",
                    "value": 25,
                    "details": f"Amount: ₹{txn.transaction_amount} | Score: {txn.prediction_score:.2f}"
                })
                edges.append({
                    "source": f"cust_{alert.customer_id}",
                    "target": f"tx_{txn.id}",
                    "type": "transact"
                })
        
        # Node 3: Security Event + Node 4: Device + Node 5: IP
        if alert.security_event_id:
            sec = db.query(SecurityEvent).filter(SecurityEvent.id == alert.security_event_id).first()
            if sec:
                nodes.append({
                    "id": f"event_{sec.id}",
                    "label": sec.event_type,
                    "type": "security_event",
                    "value": 25,
                    "details": f"Trap Score: {sec.security_trap_score:.2f}"
                })
                edges.append({
                    "source": f"cust_{alert.customer_id}",
                    "target": f"event_{sec.id}",
                    "type": "correlation"
                })
                
                # Node 4: Device fingerprint
                if sec.device_fingerprint:
                    nodes.append({
                        "id": f"dev_{sec.device_fingerprint}",
                        "label": sec.device_fingerprint[:12],
                        "type": "device",
                        "value": 15,
                        "details": f"Device: {sec.device_fingerprint}"
                    })
                    edges.append({
                        "source": f"event_{sec.id}",
                        "target": f"dev_{sec.device_fingerprint}",
                        "type": "used_device"
                    })
                
                # Node 5: IP Address
                if sec.ip_address:
                    nodes.append({
                        "id": f"ip_{sec.ip_address}",
                        "label": sec.ip_address,
                        "type": "ip",
                        "value": 15,
                        "details": f"IP: {sec.ip_address} | Geo: {sec.geo_location or 'Unknown'}"
                    })
                    edges.append({
                        "source": f"event_{sec.id}",
                        "target": f"ip_{sec.ip_address}",
                        "type": "login_from"
                    })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "alert_id": alert_id
        }
    except HTTPException:
        raise
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
    from models import CorrelatedAlert
    from datetime import datetime, timedelta
    
    try:
        # Get all alerts
        alerts = db.query(CorrelatedAlert).all()
        
        total_alerts = len(alerts)
        critical_alerts = len([a for a in alerts if a.risk_level == "Critical"])
        high_alerts = len([a for a in alerts if a.risk_level == "High"])
        
        # Calculate average score
        avg_score = sum([a.correlated_score for a in alerts]) / total_alerts if total_alerts > 0 else 0.0
        
        # Alerts by hour (last 24 hours)
        alerts_by_hour = []
        for i in range(24):
            alerts_by_hour.append(0)
        
        for alert in alerts:
            if alert.created_at:
                hour_diff = (datetime.utcnow() - alert.created_at).total_seconds() / 3600
                if hour_diff < 24:
                    idx = min(int(hour_diff), 23)
                    alerts_by_hour[23 - idx] += 1
        
        # Top risk customers (group by customer_id)
        customer_risks = {}
        for alert in alerts:
            if alert.customer_id not in customer_risks:
                customer_risks[alert.customer_id] = {"count": 0, "avg_score": 0.0, "max_risk": "Low"}
            customer_risks[alert.customer_id]["count"] += 1
            customer_risks[alert.customer_id]["avg_score"] = (
                customer_risks[alert.customer_id]["avg_score"] + alert.correlated_score
            ) / 2
            
            risk_levels = ["Low", "Medium", "High", "Critical"]
            try:
                if risk_levels.index(alert.risk_level) > risk_levels.index(customer_risks[alert.customer_id]["max_risk"]):
                    customer_risks[alert.customer_id]["max_risk"] = alert.risk_level
            except ValueError:
                pass
        
        top_risk_customers = sorted(
            [{"customer_id": cid, **data} for cid, data in customer_risks.items()],
            key=lambda x: x["avg_score"],
            reverse=True
        )[:5]
        
        return {
            "total_alerts": total_alerts,
            "critical_alerts": critical_alerts,
            "high_alerts": high_alerts,
            "avg_correlated_score": round(avg_score, 2),
            "alerts_by_hour": alerts_by_hour,
            "top_risk_customers": top_risk_customers
        }
    except Exception as e:
        logger.error(f"❌ Analytics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== SEED DATA ENDPOINT (for testing) =====

@app.post("/api/seed-data", tags=["Testing"])
async def seed_test_data(db: Session = Depends(get_db)):
    """
    Populate test data (transactions + security events + alerts) for demo
    WARNING: Only enable in development
    """
    from datetime import datetime, timedelta
    from models import Transaction, SecurityEvent, CorrelatedAlert
    
    try:
        # Clear existing data
        db.query(CorrelatedAlert).delete()
        db.query(Transaction).delete()
        db.query(SecurityEvent).delete()
        db.commit()
        
        # Create test transactions
        transactions = []
        for i in range(15):
            tx_datetime = datetime.utcnow() - timedelta(hours=i*2)
            tx = Transaction(
                customer_id=f"CUST{1000+i}",
                email=f"customer{i}@example.com",
                transaction_id=f"TXN{10000+i}",
                transaction_amount=float(100 + i*50),
                transaction_datetime=tx_datetime,
                prediction_score=0.3 + (i % 5) * 0.15,
                is_fraud=1 if (i % 5 == 0) else 0,
                combined_score=0.3 + (i % 5) * 0.15
            )
            transactions.append(tx)
            db.add(tx)
        db.commit()
        
        # Create test security events
        security_events = []
        for i in range(10):
            event_time = datetime.utcnow() - timedelta(hours=i*3)
            event = SecurityEvent(
                customer_id=f"CUST{1000+i}",
                email=f"customer{i}@example.com",
                event_type=["login", "failed_login", "session_start"][i % 3],
                device_fingerprint=f"DEV{5000+i}",
                ip_address=f"192.168.{i}.{100+i}",
                security_trap_score=0.2 + (i % 4) * 0.2,
                event_timestamp=event_time
            )
            security_events.append(event)
            db.add(event)
        db.commit()
        
        # Create correlated alerts
        alerts = []
        for i in range(8):
            alert = CorrelatedAlert(
                customer_id=f"CUST{1000+i}",
                transaction_id=transactions[i].id if i < len(transactions) else None,
                security_event_id=security_events[i].id if i < len(security_events) else None,
                correlation_window_sec=900,
                correlated_score=0.4 + (i % 4) * 0.15,
                risk_level=["Low", "Medium", "High", "Critical"][i % 4],
                explanation=f"Suspicious transaction from customer {i} with concurrent security event",
                status="open"
            )
            alerts.append(alert)
            db.add(alert)
        db.commit()
        
        return {
            "transactions_created": len(transactions),
            "security_events_created": len(security_events),
            "alerts_created": len(alerts),
            "message": "✅ Test data seeded successfully"
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
