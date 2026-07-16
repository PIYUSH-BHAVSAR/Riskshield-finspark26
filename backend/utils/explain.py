from datetime import datetime

def generate_correlated_explanation(sec_event, txn, gap_sec, correlated_score, risk_level) -> str:
    """
    Generates a structured, human-readable text explanation of why a correlation was flagged.
    """
    sec_time = sec_event.event_timestamp
    if isinstance(sec_time, str):
        sec_time = datetime.fromisoformat(sec_time)
    sec_time_str = sec_time.strftime("%H:%M:%S")
    
    txn_time = txn.transaction_datetime
    if isinstance(txn_time, str):
        txn_time = datetime.fromisoformat(txn_time)
    txn_time_str = txn_time.strftime("%H:%M:%S")
    
    gap_min = gap_sec // 60
    gap_rem_sec = gap_sec % 60
    gap_str = f"{gap_min}m {gap_rem_sec}s" if gap_min > 0 else f"{gap_rem_sec}s"
    
    # Extract flag details
    hard_flags_str = ", ".join(sec_event.hard_flags) if sec_event.hard_flags else "unusual activity"
    if sec_event.iso_anomaly_flag == 1:
        hard_flags_str += " (statistical outlier)"
        
    # Transaction rules triggered
    tx_rules_str = ", ".join(txn.rules_triggered) if txn.rules_triggered else "standard transfer"
    
    explanation = (
        f"⚠️ Temporal Correlation Alert ({risk_level} Risk - Score: {correlated_score:.2f})\n\n"
        f"1. Telemetry Flag: '{hard_flags_str}' detected on account for customer {sec_event.customer_id} "
        f"from IP {sec_event.ip_address} ({sec_event.geo_location}) at {sec_time_str}.\n"
        f"2. Transaction Event: A transfer of ₹{txn.transaction_amount:,.2f} via channel {txn.channel_encoded} "
        f"({tx_rules_str}) occurred at {txn_time_str} with combined score {txn.combined_score:.2f}.\n"
        f"3. Timeline Correlation: Transaction occurred {gap_str} after the suspicious security event. "
        f"The rapid velocity between the access event and transactional activity indicates highly probable account takeover."
    )
    
    return explanation
