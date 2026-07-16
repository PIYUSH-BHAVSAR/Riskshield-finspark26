import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session

# Add parent directory to path to allow importing backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import Base, engine, SessionLocal
from backend.models import User, Transaction, SecurityEvent, CorrelatedAlert
from backend.data.generate_data import generate_dataset
from backend.utils.tx_features import extract_features
from backend.utils.security_rules import run_all_rules
from backend.utils.isolation_forest import train_isolation_forest, predict_anomaly, engineer_features
from backend.utils.correlation_engine import run_correlation_engine

# Import password hashing helper
import bcrypt

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model")
CATBOOST_MODEL_PATH = os.path.join(MODEL_DIR, "catboost_fraud_model_balanced_tuned.cbm")

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def train_catboost_model(transactions_data: list):
    """
    Trains a baseline CatBoost model on the synthetic transaction data.
    """
    print("Training CatBoost transaction fraud model...")
    from catboost import CatBoostClassifier
    
    # Labelling fraud based on synthetic generation features:
    # Large amount, off-hours, channel 0/1
    labels = []
    features_list = []
    
    for tx in transactions_data:
        # Features extraction
        features = extract_features(tx)
        features_list.append(features.iloc[0])
        
        # Check if this transaction fits the fraud characteristics we generated
        amount = tx["transaction_amount"]
        dt = datetime.fromisoformat(tx["transaction_datetime"])
        off_hours = dt.hour in [0, 1, 2, 3, 4, 23]
        if amount > 50000 and off_hours:
            labels.append(1)
        else:
            labels.append(0)
            
    X = pd.DataFrame(features_list)
    y = np.array(labels)
    
    # Train model
    clf = CatBoostClassifier(iterations=60, depth=4, learning_rate=0.1, verbose=0, random_seed=42)
    clf.fit(X, y)
    
    # Ensure model folder exists
    os.makedirs(MODEL_DIR, exist_ok=True)
    clf.save_model(CATBOOST_MODEL_PATH)
    print(f"CatBoost model saved to {CATBOOST_MODEL_PATH}")
    return clf

def main():
    print("Initializing Database tables...")
    Base.metadata.drop_all(bind=engine) # Start fresh
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Create Default Admin User
        admin_email = "admin@riskshield.com"
        admin = db.query(User).filter(User.email == admin_email).first()
        if not admin:
            print("Creating default admin user (admin@riskshield.com / admin123)...")
            admin = User(
                email=admin_email,
                hashed_password=hash_password("admin123"),
                full_name="RiskShield Admin",
                role="admin"
            )
            db.add(admin)
            db.commit()
            
        # 2. Generate Synthetic Datasets
        print("Generating synthetic datasets...")
        customers, transactions, security_events = generate_dataset(
            num_customers=50,
            num_transactions=400,
            fraud_rate=0.08
        )
        
        # Train and save the CatBoost model on transaction data
        catboost_model = train_catboost_model(transactions)
        
        # 3. Insert customers as users so foreign key references work
        print("Seeding customer accounts into users...")
        hashed_cust_pwd = hash_password("customer123")
        customer_emails = set()
        
        for cust in customers:
            # Avoid inserting admin duplicate
            if cust["email"] == admin_email:
                continue
            user = User(
                email=cust["email"],
                hashed_password=hashed_cust_pwd,
                full_name=cust["full_name"],
                role="customer"
            )
            db.add(user)
            customer_emails.add(cust["email"])
        db.commit()
        
        # 4. Process and Seed Transactions
        print("Evaluating and seeding transactions...")
        # Prepare feature engineering for batch prediction
        features_df = extract_features(transactions)
        pred_probas = catboost_model.predict_proba(features_df)[:, 1]
        
        seeded_tx_map = {}
        for idx, tx in enumerate(transactions):
            score = float(pred_probas[idx])
            
            # Simple heuristic transaction rules
            rules = []
            if tx["transaction_amount"] > 100000:
                rules.append("HIGH_VALUE")
            dt = datetime.fromisoformat(tx["transaction_datetime"])
            if dt.hour in [0, 1, 2, 3, 4, 23]:
                rules.append("OFF_HOURS")
            if tx["kyc_verified"] == 0:
                rules.append("UNVERIFIED_KYC")
                
            combined_score = min(1.0, score + 0.1 * len(rules))
            is_fraud_flag = 1 if combined_score >= 0.6 else 0
            
            db_tx = Transaction(
                customer_id=tx["customer_id"],
                email=tx["email"],
                transaction_id=tx["transaction_id"],
                transaction_amount=tx["transaction_amount"],
                transaction_datetime=dt,
                kyc_verified=tx["kyc_verified"],
                account_age_days=tx["account_age_days"],
                channel_encoded=tx["channel_encoded"],
                prediction_score=score,
                is_fraud=is_fraud_flag,
                rules_triggered=rules,
                combined_score=combined_score
            )
            db.add(db_tx)
            seeded_tx_map[tx["transaction_id"]] = db_tx
            
        db.commit()
        
        # 5. Fit Isolation Forest on security events and save it
        print("Training Isolation Forest telemetry model...")
        # To simulate historical events context, we iterate through and compute historical metrics
        history_events = []
        history_contexts = []
        cust_event_history = {} # customer_id -> list of events
        
        for ev in security_events:
            cust_id = ev["customer_id"]
            if cust_id not in cust_event_history:
                cust_event_history[cust_id] = []
                
            cust_history = cust_event_history[cust_id]
            known_devices = {x["device_fingerprint"] for x in cust_history}
            last_event = cust_history[-1] if cust_history else None
            
            # Count failed attempts in the last hour
            t_curr = datetime.fromisoformat(ev["event_timestamp"])
            failed_1h = sum(
                1 for x in cust_history
                if x["event_type"] == "failed_login" and 
                (t_curr - datetime.fromisoformat(x["event_timestamp"])).total_seconds() < 3600
            )
            
            context = {
                "known_devices": known_devices,
                "last_event": last_event,
                "failed_attempts_last_hour": failed_1h + ev.get("_failed_attempts_last_hour", 0)
            }
            
            history_events.append(ev)
            history_contexts.append(context)
            cust_event_history[cust_id].append(ev)
            
        train_isolation_forest(history_events, history_contexts)
        
        # 6. Seed Security Events
        print("Evaluating and seeding security events...")
        # Reloading contexts and applying isolation forest + rule evaluation
        for idx, ev in enumerate(security_events):
            context = history_contexts[idx]
            
            # Predict isolation forest anomaly flag
            iso_flag = predict_anomaly(ev, context)
            
            # Run rules
            hard_flags = run_all_rules(ev, context)
            
            # Compute trap score
            trap_score = float(len(hard_flags) + iso_flag)
            
            db_ev = SecurityEvent(
                customer_id=ev["customer_id"],
                email=ev["email"],
                event_type=ev["event_type"],
                device_fingerprint=ev["device_fingerprint"],
                ip_address=ev["ip_address"],
                geo_location=ev["geo_location"],
                hard_flags=hard_flags,
                iso_anomaly_flag=iso_flag,
                security_trap_score=trap_score,
                event_timestamp=datetime.fromisoformat(ev["event_timestamp"])
            )
            db.add(db_ev)
            
        db.commit()
        
        # 7. Run Correlation Engine to establish links
        print("Running correlation engine...")
        new_alerts = run_correlation_engine(db)
        print(f"Created {new_alerts} correlated alerts in database.")
        
        print("\nSeeding complete! Database is fully set up and models are trained.")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
