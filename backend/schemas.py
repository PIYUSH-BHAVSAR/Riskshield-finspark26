from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

# Base ORM config compatible with Pydantic v1 & v2
class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Optional[str] = "analyst"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseSchema):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Transaction Schemas
class TransactionCreate(BaseModel):
    customer_id: str
    email: Optional[str] = None
    transaction_id: str
    transaction_amount: float
    transaction_datetime: datetime
    kyc_verified: Optional[int] = 1
    account_age_days: Optional[int] = 365
    channel_encoded: Optional[int] = 0

class TransactionResponse(BaseSchema):
    id: int
    customer_id: str
    email: Optional[str]
    transaction_id: str
    transaction_amount: float
    transaction_datetime: datetime
    kyc_verified: int
    account_age_days: int
    channel_encoded: int
    prediction_score: float
    is_fraud: int
    rules_triggered: List[str]
    combined_score: float
    created_at: datetime

# Security Event Schemas
class SecurityEventCreate(BaseModel):
    customer_id: str
    email: str
    event_type: str  # login, failed_login, session_start
    device_fingerprint: str
    ip_address: str
    geo_location: str
    event_timestamp: Optional[datetime] = None

class SecurityEventResponse(BaseSchema):
    id: int
    customer_id: str
    email: str
    event_type: str
    device_fingerprint: str
    ip_address: str
    geo_location: str
    hard_flags: List[str]
    iso_anomaly_flag: int
    security_trap_score: float
    event_timestamp: datetime

# Correlated Alert Schemas
class CorrelatedAlertResponse(BaseSchema):
    id: int
    customer_id: str
    transaction_id: Optional[int]
    security_event_id: Optional[int]
    correlation_window_sec: int
    correlated_score: float
    explanation: str
    risk_level: str
    status: str
    created_at: datetime
    
    transaction: Optional[TransactionResponse] = None
    security_event: Optional[SecurityEventResponse] = None

# Dashboard Analytics Schema
class AnalyticsResponse(BaseModel):
    total_alerts: int
    critical_alerts: int
    high_alerts: int
    medium_alerts: int
    low_alerts: int
    average_risk_score: float
    system_status: str  # healthy, warning, degraded
    risk_distribution: List[dict]  # list of dicts for charting
    alerts_trend: List[dict]        # list of daily trend data
