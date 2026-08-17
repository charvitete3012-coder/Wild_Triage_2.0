# anomaly_engine.py

def evaluate_alerts(records):
    """
    Scans camera records for boundary breaches and anomaly conditions.
    """
    alerts = []
    
    for rec in records:
        if rec["is_blank"]:
            continue
            
        # Rule 1: Village Proximity Alert
        if rec.get("station_type") == "village_adjacent":
            alerts.append({
                "level": "CRITICAL",
                "title": "Village Boundary Breach",
                "desc": f"Detection of **{rec['tiger_id']}** at village-adjacent station `{rec['station_id']}`."
            })
            
        # Rule 2: Absence Return Alert
        if rec.get("last_seen_days", 0) > 30:
            alerts.append({
                "level": "WARNING",
                "title": "Prolonged Absence Spotted",
                "desc": f"**{rec['tiger_id']}** re-appeared after **{rec['last_seen_days']} days** of inactivity."
            })
            
    return alerts