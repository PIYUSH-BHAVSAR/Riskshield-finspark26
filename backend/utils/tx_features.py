import pandas as pd
from datetime import datetime

def extract_features(tx_data: dict) -> pd.DataFrame:
    """
    Extracts a feature DataFrame for a single transaction or a list of transactions.
    Expects input dict/list with keys:
      - transaction_amount
      - kyc_verified
      - account_age_days
      - channel_encoded
      - transaction_datetime (string or datetime object)
    """
    # Normalize input to list of dicts
    if isinstance(tx_data, dict):
        data = [tx_data]
    else:
        data = tx_data
        
    df = pd.DataFrame(data)
    
    # Parse datetime
    if "transaction_datetime" in df.columns:
        df["dt"] = pd.to_datetime(df["transaction_datetime"])
        df["hour_of_day"] = df["dt"].dt.hour
        df["is_weekend"] = df["dt"].dt.dayofweek.isin([5, 6]).astype(int)
    else:
        df["hour_of_day"] = datetime.now().hour
        df["is_weekend"] = int(datetime.now().weekday() in [5, 6])
        
    # Drop temp columns
    if "dt" in df.columns:
        df = df.drop(columns=["dt"])
        
    # Ensure correct columns exist and are ordered
    feature_cols = [
        "transaction_amount",
        "kyc_verified",
        "account_age_days",
        "channel_encoded",
        "hour_of_day",
        "is_weekend"
    ]
    
    # Fill missing columns if any
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0
            
    return df[feature_cols]
