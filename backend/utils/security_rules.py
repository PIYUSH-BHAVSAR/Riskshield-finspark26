from datetime import datetime

def check_new_device(event: dict, known_devices: set) -> bool:
    """
    Checks if the device fingerprint has never been seen before for this customer.
    """
    if not known_devices:
        return False
    return event.get("device_fingerprint") not in known_devices

def check_impossible_travel(event: dict, last_event: dict) -> bool:
    """
    Checks if the customer logged in from a different geo-location in less than 2 hours.
    """
    if not last_event:
        return False
        
    loc1 = event.get("geo_location", "")
    loc2 = last_event.get("geo_location", "")
    
    if not loc1 or not loc2 or loc1 == loc2:
        return False
        
    t1 = event.get("event_timestamp")
    t2 = last_event.get("event_timestamp")
    
    if not isinstance(t1, datetime):
        t1 = datetime.fromisoformat(str(t1))
    if not isinstance(t2, datetime):
        t2 = datetime.fromisoformat(str(t2))
        
    time_gap_hr = abs((t1 - t2).total_seconds()) / 3600.0
    return time_gap_hr < 2.0

def check_credential_stuffing(failed_attempts_last_hour: int) -> bool:
    """
    Triggers if there have been 3 or more failed login attempts in the last hour.
    """
    return failed_attempts_last_hour >= 3

def check_off_hours_access(event: dict) -> bool:
    """
    Triggers if the event occurs during suspicious off-hours (11 PM - 5 AM).
    """
    t = event.get("event_timestamp")
    if not isinstance(t, datetime):
        t = datetime.fromisoformat(str(t))
    hour = t.hour
    return hour in [0, 1, 2, 3, 4, 23]

def run_all_rules(event: dict, context: dict) -> list:
    """
    Runs all deterministic checks and returns list of triggered rules.
    Context should contain:
      - 'known_devices': set of strings
      - 'last_event': dict or None
      - 'failed_attempts_last_hour': int
    """
    flags = []
    
    if check_new_device(event, context.get("known_devices", set())):
        flags.append("new_device")
        
    if check_impossible_travel(event, context.get("last_event")):
        flags.append("impossible_travel")
        
    if check_credential_stuffing(context.get("failed_attempts_last_hour", 0)):
        flags.append("credential_stuffing")
        
    if check_off_hours_access(event):
        flags.append("off_hours_access")
        
    # Standardize failed login as a flag
    if event.get("event_type") == "failed_login":
        flags.append("failed_login")
        
    return flags
