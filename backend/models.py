from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default="analyst")
    created_at = Column(DateTime, default=datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), index=True, nullable=False)
    email = Column(String(100), index=True)
    transaction_id = Column(String(50), unique=True, index=True, nullable=False)
    transaction_amount = Column(Float, nullable=False)
    transaction_datetime = Column(DateTime, nullable=False, index=True)
    kyc_verified = Column(Integer, default=1)
    account_age_days = Column(Integer, default=365)
    channel_encoded = Column(Integer, default=0)
    prediction_score = Column(Float, default=0.0)  # CatBoost output
    is_fraud = Column(Integer, default=0)
    rules_triggered = Column(JSON, default=list)   # Lists transaction rules like HIGH_VALUE
    combined_score = Column(Float, default=0.0)    # Combined risk after rules
    created_at = Column(DateTime, default=datetime.utcnow)
    
    correlated_alerts = relationship("CorrelatedAlert", back_populates="transaction")

class SecurityEvent(Base):
    __tablename__ = "security_events"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), index=True, nullable=False)
    email = Column(String(100), index=True, nullable=False)
    event_type = Column(String(30))  # login, failed_login, session_start
    device_fingerprint = Column(String(100))
    ip_address = Column(String(45))
    geo_location = Column(String(100))
    hard_flags = Column(JSON, default=list)  # e.g., ["new_device", "impossible_travel"]
    iso_anomaly_flag = Column(Integer, default=0)
    security_trap_score = Column(Float, default=0.0)
    event_timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    correlated_alerts = relationship("CorrelatedAlert", back_populates="security_event")

class CorrelatedAlert(Base):
    __tablename__ = "correlated_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), index=True, nullable=False)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    security_event_id = Column(Integer, ForeignKey("security_events.id"), nullable=True)
    correlation_window_sec = Column(Integer)
    correlated_score = Column(Float)
    explanation = Column(Text)
    risk_level = Column(String(20))  # Low, Medium, High, Critical
    status = Column(String(20), default="open")  # open, investigating, resolved, false_positive
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transaction = relationship("Transaction", back_populates="correlated_alerts")
    security_event = relationship("SecurityEvent", back_populates="correlated_alerts")
