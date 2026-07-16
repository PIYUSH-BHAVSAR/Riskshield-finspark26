import os
import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("en_IN")

def generate_dataset(num_customers=60, num_transactions=500, fraud_rate=0.08):
    """
    Generates a linked set of customers, transactions, and security events.
    Produces VARIED fraud severity tiers to demonstrate the scoring engine's
    ability to differentiate risk levels (Critical, High, Medium, Low).
    """
    random.seed(42)
    
    # 1. Generate Customers
    customers = []
    for i in range(num_customers):
        customer_id = f"CUST{1000 + i}"
        customers.append({
            "customer_id": customer_id,
            "email": f"cust_{1000 + i}@example.com",
            "full_name": fake.name(),
            "kyc_verified": random.choice([1, 1, 1, 0]),  # 25% unverified
            "account_age_days": random.randint(15, 1200)
        })
        
    # Track device history per customer
    customer_devices = {}
    for c in customers:
        customer_devices[c["customer_id"]] = [fake.uuid4()[:16], fake.uuid4()[:16]]
        
    transactions = []
    security_events = []
    
    num_fraud = int(num_transactions * fraud_rate)
    num_normal = num_transactions - num_fraud
    
    # 2. Generate Normal Transactions
    for i in range(num_normal):
        cust = random.choice(customers)
        cust_id = cust["customer_id"]
        
        # Normal amount: 50 to 15,000
        amount = round(random.uniform(50, 15000), 2)
        # Normal hour range: 7 AM to 10 PM
        hour = random.randint(7, 22)
        dt = datetime.now() - timedelta(
            days=random.randint(1, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        dt = dt.replace(hour=hour)
        
        tx_id = f"TXN{random.randint(100000, 999999)}"
        txn = {
            "customer_id": cust_id,
            "email": cust["email"],
            "transaction_id": tx_id,
            "transaction_amount": amount,
            "transaction_datetime": dt.isoformat(),
            "kyc_verified": cust["kyc_verified"],
            "account_age_days": cust["account_age_days"],
            "channel_encoded": random.choice([0, 1, 2, 3])
        }
        transactions.append(txn)
        
        # Generate ordinary login events leading up to transaction
        if random.random() < 0.4:
            login_time = dt - timedelta(minutes=random.randint(10, 180))
            device = random.choice(customer_devices[cust_id])
            event = {
                "customer_id": cust_id,
                "email": cust["email"],
                "event_type": "login",
                "device_fingerprint": device,
                "ip_address": f"192.168.1.{random.randint(2, 254)}",
                "geo_location": "Mumbai, IN",
                "event_timestamp": login_time.isoformat(),
                "_failed_attempts_last_hour": 0
            }
            security_events.append(event)
            
    # 3. Generate Fraudulent Transactions with VARIED severity tiers
    # Split fraud into 4 tiers to produce a realistic risk distribution:
    #   Tier 1 (Critical): Full attack - new device + impossible travel + off-hours + high amount + brute force
    #   Tier 2 (High):     Partial attack - new device + off-hours + moderate-high amount, NO impossible travel
    #   Tier 3 (Medium):   Weak signal - new device only + business-hours + moderate amount, wider gap
    #   Tier 4 (Low):      Borderline - known device from unusual geo, small amount, edge of window
    
    tier_sizes = [
        int(num_fraud * 0.25),   # ~25% Critical (full attack stack)
        int(num_fraud * 0.30),   # ~30% High
        int(num_fraud * 0.25),   # ~25% Medium
    ]
    tier_sizes.append(num_fraud - sum(tier_sizes))  # remainder -> Low
    
    fraud_idx = 0
    
    # --- TIER 1: CRITICAL (full attack) ---
    for i in range(tier_sizes[0]):
        cust = random.choice(customers)
        cust_id = cust["customer_id"]
        
        # Very high value: 150K-350K, off-hours
        amount = round(random.uniform(150000, 350000), 2)
        hour = random.choice([0, 1, 2, 3, 4, 23])
        dt = datetime.now() - timedelta(
            days=random.randint(1, 30),
            hours=random.randint(0, 5),
            minutes=random.randint(0, 59)
        )
        dt = dt.replace(hour=hour)
        
        tx_id = f"TXN{random.randint(100000, 999999)}"
        txn = {
            "customer_id": cust_id,
            "email": cust["email"],
            "transaction_id": tx_id,
            "transaction_amount": amount,
            "transaction_datetime": dt.isoformat(),
            "kyc_verified": 0,  # Unverified KYC for max severity
            "account_age_days": cust["account_age_days"],
            "channel_encoded": random.choice([0, 1])
        }
        transactions.append(txn)
        
        # Security event: 2-5 min before, new device, foreign geo, brute force
        time_gap = random.randint(2, 5)
        sec_time = dt - timedelta(minutes=time_gap)
        new_device = fake.uuid4()[:16]
        geo = random.choice(["Lagos, NG", "Manila, PH", "Bucharest, RO", "Kiev, UA"])
        
        sec_event = {
            "customer_id": cust_id,
            "email": cust["email"],
            "event_type": "failed_login",
            "device_fingerprint": new_device,
            "ip_address": f"{random.randint(45, 185)}.{random.randint(10, 200)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
            "geo_location": geo,
            "event_timestamp": sec_time.isoformat(),
            "_failed_attempts_last_hour": random.choice([3, 4, 5])
        }
        security_events.append(sec_event)
        
        # Preceding India login to trigger IMPOSSIBLE TRAVEL
        prev_time = sec_time - timedelta(minutes=65)
        prev_event = {
            "customer_id": cust_id,
            "email": cust["email"],
            "event_type": "login",
            "device_fingerprint": random.choice(customer_devices[cust_id]),
            "ip_address": f"103.45.{random.randint(1, 254)}.{random.randint(1, 254)}",
            "geo_location": "Pune, IN",
            "event_timestamp": prev_time.isoformat(),
            "_failed_attempts_last_hour": 0
        }
        security_events.append(prev_event)
    
    # --- TIER 2: HIGH (new device + off-hours, NO impossible travel) ---
    for i in range(tier_sizes[1]):
        cust = random.choice(customers)
        cust_id = cust["customer_id"]
        
        # Moderate-high value: 50K-150K, off-hours
        amount = round(random.uniform(50000, 150000), 2)
        hour = random.choice([0, 1, 2, 3, 23])
        dt = datetime.now() - timedelta(
            days=random.randint(1, 30),
            hours=random.randint(0, 5),
            minutes=random.randint(0, 59)
        )
        dt = dt.replace(hour=hour)
        
        tx_id = f"TXN{random.randint(100000, 999999)}"
        txn = {
            "customer_id": cust_id,
            "email": cust["email"],
            "transaction_id": tx_id,
            "transaction_amount": amount,
            "transaction_datetime": dt.isoformat(),
            "kyc_verified": cust["kyc_verified"],
            "account_age_days": cust["account_age_days"],
            "channel_encoded": random.choice([0, 1])
        }
        transactions.append(txn)
        
        # Security event: 3-8 min before, new device, same country but different city
        time_gap = random.randint(3, 8)
        sec_time = dt - timedelta(minutes=time_gap)
        new_device = fake.uuid4()[:16]
        geo = random.choice(["Delhi, IN", "Kolkata, IN", "Chennai, IN", "Hyderabad, IN"])
        
        sec_event = {
            "customer_id": cust_id,
            "email": cust["email"],
            "event_type": random.choice(["login", "failed_login"]),
            "device_fingerprint": new_device,
            "ip_address": f"103.{random.randint(10, 250)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
            "geo_location": geo,
            "event_timestamp": sec_time.isoformat(),
            "_failed_attempts_last_hour": random.choice([0, 1, 2])  # Below brute-force threshold
        }
        security_events.append(sec_event)
        # NO preceding impossible-travel event for this tier
    
    # --- TIER 3: MEDIUM (new device only, business hours, moderate amount) ---
    for i in range(tier_sizes[2]):
        cust = random.choice(customers)
        cust_id = cust["customer_id"]
        
        # Moderate amount: 20K-75K, business hours
        amount = round(random.uniform(20000, 75000), 2)
        hour = random.randint(9, 18)
        dt = datetime.now() - timedelta(
            days=random.randint(1, 30),
            hours=random.randint(0, 12),
            minutes=random.randint(0, 59)
        )
        dt = dt.replace(hour=hour)
        
        tx_id = f"TXN{random.randint(100000, 999999)}"
        txn = {
            "customer_id": cust_id,
            "email": cust["email"],
            "transaction_id": tx_id,
            "transaction_amount": amount,
            "transaction_datetime": dt.isoformat(),
            "kyc_verified": cust["kyc_verified"],
            "account_age_days": cust["account_age_days"],
            "channel_encoded": random.choice([0, 1, 2])
        }
        transactions.append(txn)
        
        # Security event: 8-13 min before (wider gap), new device, same region
        time_gap = random.randint(8, 13)
        sec_time = dt - timedelta(minutes=time_gap)
        new_device = fake.uuid4()[:16]
        geo = random.choice(["Mumbai, IN", "Pune, IN", "Nagpur, IN"])
        
        sec_event = {
            "customer_id": cust_id,
            "email": cust["email"],
            "event_type": "login",  # Regular login, not failed
            "device_fingerprint": new_device,
            "ip_address": f"103.45.{random.randint(1, 254)}.{random.randint(1, 254)}",
            "geo_location": geo,
            "event_timestamp": sec_time.isoformat(),
            "_failed_attempts_last_hour": 0
        }
        security_events.append(sec_event)
    
    # --- TIER 4: LOW (known device, unusual geo, small amount, edge of window) ---
    for i in range(tier_sizes[3]):
        cust = random.choice(customers)
        cust_id = cust["customer_id"]
        
        # Low amount: 5K-25K, business hours
        amount = round(random.uniform(5000, 25000), 2)
        hour = random.randint(8, 20)
        dt = datetime.now() - timedelta(
            days=random.randint(1, 30),
            hours=random.randint(0, 12),
            minutes=random.randint(0, 59)
        )
        dt = dt.replace(hour=hour)
        
        tx_id = f"TXN{random.randint(100000, 999999)}"
        txn = {
            "customer_id": cust_id,
            "email": cust["email"],
            "transaction_id": tx_id,
            "transaction_amount": amount,
            "transaction_datetime": dt.isoformat(),
            "kyc_verified": 1,  # KYC verified
            "account_age_days": cust["account_age_days"],
            "channel_encoded": random.choice([0, 1, 2, 3])
        }
        transactions.append(txn)
        
        # Security event: 11-14 min before (edge of 15-min window), KNOWN device, slightly unusual geo
        time_gap = random.randint(11, 14)
        sec_time = dt - timedelta(minutes=time_gap)
        known_device = random.choice(customer_devices[cust_id])  # KNOWN device
        geo = random.choice(["Bangalore, IN", "Ahmedabad, IN"])
        
        sec_event = {
            "customer_id": cust_id,
            "email": cust["email"],
            "event_type": "login",
            "device_fingerprint": known_device,
            "ip_address": f"103.45.{random.randint(1, 254)}.{random.randint(1, 254)}",
            "geo_location": geo,
            "event_timestamp": sec_time.isoformat(),
            "_failed_attempts_last_hour": 0
        }
        security_events.append(sec_event)
        
    # Sort datasets chronologically
    transactions.sort(key=lambda x: x["transaction_datetime"])
    security_events.sort(key=lambda x: x["event_timestamp"])
    
    return customers, transactions, security_events

if __name__ == "__main__":
    customers, transactions, security_events = generate_dataset()
    
    # Save to JSON files inside backend/data
    data_dir = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(data_dir, "customers.json"), "w") as f:
        json.dump(customers, f, indent=2)
        
    with open(os.path.join(data_dir, "transactions.json"), "w") as f:
        json.dump(transactions, f, indent=2)
        
    with open(os.path.join(data_dir, "security_events.json"), "w") as f:
        json.dump(security_events, f, indent=2)
        
    print(f"Generated {len(customers)} customers, {len(transactions)} transactions, and {len(security_events)} security events successfully.")
