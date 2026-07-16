import os
import pickle
import numpy as np
from sklearn.ensemble import IsolationForest

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "model")
MODEL_PATH = os.path.join(MODEL_DIR, "isolation_forest.pkl")

FEATURE_ORDER = [
    "failed_login_count_1h",
    "device_novelty_flag",
    "hour_of_day",
    "is_off_hours"
]

def engineer_features(event: dict, context: dict) -> list:
    """
    Extracts numerical features from a security event and its context.
    """
    failed_login_count_1h = float(context.get("failed_attempts_last_hour", 0))
    
    known_devices = context.get("known_devices", set())
    device_fingerprint = event.get("device_fingerprint", "")
    device_novelty_flag = 1.0 if (known_devices and device_fingerprint not in known_devices) else 0.0
    
    t = event.get("event_timestamp")
    if not t:
        from datetime import datetime
        t = datetime.now()
    elif isinstance(t, str):
        from datetime import datetime
        t = datetime.fromisoformat(t)
        
    hour_of_day = float(t.hour)
    is_off_hours = 1.0 if hour_of_day in [0, 1, 2, 3, 4, 23] else 0.0
    
    return [failed_login_count_1h, device_novelty_flag, hour_of_day, is_off_hours]

def train_isolation_forest(events_data: list, contexts: list):
    """
    Fits Isolation Forest on historical data and saves to disk.
    """
    X = []
    for ev, ctx in zip(events_data, contexts):
        X.append(engineer_features(ev, ctx))
        
    X = np.array(X)
    
    # 5% contamination target for suspicious events
    clf = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    clf.fit(X)
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(clf, f)
        
    return clf

def predict_anomaly(event: dict, context: dict) -> int:
    """
    Infers anomalous status of a security event.
    Returns 1 if anomalous (-1 in IsolationForest terms), 0 otherwise.
    """
    features = np.array([engineer_features(event, context)])
    
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                clf = pickle.load(f)
            pred = clf.predict(features)
            return 1 if pred[0] == -1 else 0
    except Exception as e:
        print(f"Error loading Isolation Forest: {e}")
        
    # Heuristic fallback if model is missing or fails to load
    # Flag as anomaly if there are multiple failed logins or a new device during off hours
    failed_attempts = features[0][0]
    new_device = features[0][1]
    off_hours = features[0][3]
    
    if failed_attempts >= 3.0:
        return 1
    if new_device == 1.0 and off_hours == 1.0:
        return 1
        
    return 0
