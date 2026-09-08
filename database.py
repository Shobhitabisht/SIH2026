"""
SQLite Data Store & Seed Data Provider
Maintains persistence for farmer diagnosis reports, expert validations, and broadcast alerts.
"""

import sqlite3
import json
import uuid
from datetime import datetime
from backend.app.config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Reports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id TEXT PRIMARY KEY,
        farmer_name TEXT,
        village TEXT,
        crop TEXT,
        growth_stage TEXT,
        disease_id TEXT,
        disease_name TEXT,
        confidence REAL,
        farm_risk_score REAL,
        risk_level TEXT,
        temperature_c REAL,
        humidity_pct REAL,
        iot_trap_count INTEGER,
        latitude REAL,
        longitude REAL,
        expert_status TEXT,
        xai_breakdown TEXT,
        advisory_payload TEXT,
        created_at TEXT
    )
    """)

    # Broadcast alerts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id TEXT PRIMARY KEY,
        target_village TEXT,
        radius_km REAL,
        alert_title TEXT,
        message_hi TEXT,
        message_en TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    
    # Check if empty, populate with seed data for hackathon demo
    cursor.execute("SELECT COUNT(*) FROM reports")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_reports(conn)
        
    conn.close()

def seed_reports(conn):
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()

    sample_reports = [
        (
            "REP-101", "Ramesh Patil", "Jalna Central", "rice", "vegetative",
            "rice_blast", "Rice Blast (Magnaporthe oryzae)", 0.92, 0.88, "High",
            30.2, 88.0, 56, 19.7515, 75.7139, "AI-Flagged",
            json.dumps([{"factor": "Image AI", "signal": "Rice Blast 92%"}, {"factor": "Humidity", "signal": "88% Moisture"}]),
            json.dumps({"disease_name": "धान का झुलसा रोग", "dos": ["ट्राइसाइक्लाज़ोल का छिड़काव करें।"]}),
            now
        ),
        (
            "REP-102", "Suresh Deshmukh", "Ambad Tehsil", "wheat", "flowering",
            "wheat_yellow_rust", "Wheat Yellow Rust", 0.89, 0.79, "High",
            24.5, 82.0, 38, 19.6100, 75.7900, "Verified - Confirmed",
            json.dumps([{"factor": "Image AI", "signal": "Yellow Rust 89%"}, {"factor": "Weather", "signal": "Cool humid morning"}]),
            json.dumps({"disease_name": "गेहूं का पीला रतुआ", "dos": ["प्रोपिकोनाज़ोल का छिड़काव करें।"]}),
            now
        ),
        (
            "REP-103", "Anita Shinde", "Partur District", "tomato", "fruiting",
            "tomato_late_blight", "Tomato Late Blight", 0.94, 0.84, "High",
            27.0, 91.0, 42, 19.5800, 76.0100, "AI-Flagged",
            json.dumps([{"factor": "Image AI", "signal": "Late Blight 94%"}, {"factor": "Humidity", "signal": "91% Extreme"}]),
            json.dumps({"disease_name": "टमाटर का पछैती झुलसा", "dos": ["मैनकोज़ेब का छिड़काव करें।"]}),
            now
        ),
        (
            "REP-104", "Vijay Kumar", "Badnapur", "cotton", "vegetative",
            "healthy", "Healthy Crop", 0.95, 0.12, "Low",
            31.0, 60.0, 12, 19.8700, 75.5400, "Verified - Confirmed",
            json.dumps([{"factor": "Image AI", "signal": "Healthy Canopy 95%"}]),
            json.dumps({"disease_name": "स्वास्थ्य फसल", "dos": ["नियमित देखभाल जारी रखें।"]}),
            now
        ),
        (
            "REP-105", "Gurpreet Singh", "Khadki Village", "potato", "vegetative",
            "potato_early_blight", "Potato Early Blight", 0.85, 0.58, "Medium",
            28.0, 74.0, 29, 19.7800, 75.8200, "AI-Flagged",
            json.dumps([{"factor": "Image AI", "signal": "Early Blight 85%"}]),
            json.dumps({"disease_name": "आलू का अगेती झुलसा", "dos": ["क्लोरोथेलोनिल का छिड़काव करें।"]}),
            now
        )
    ]

    cursor.executemany("""
    INSERT INTO reports (
        id, farmer_name, village, crop, growth_stage, disease_id, disease_name,
        confidence, farm_risk_score, risk_level, temperature_c, humidity_pct,
        iot_trap_count, latitude, longitude, expert_status, xai_breakdown,
        advisory_payload, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_reports)

    conn.commit()

def save_report(data: dict) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    report_id = f"REP-{uuid.uuid4().hex[:6].upper()}"
    now = datetime.utcnow().isoformat()

    cursor.execute("""
    INSERT INTO reports (
        id, farmer_name, village, crop, growth_stage, disease_id, disease_name,
        confidence, farm_risk_score, risk_level, temperature_c, humidity_pct,
        iot_trap_count, latitude, longitude, expert_status, xai_breakdown,
        advisory_payload, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id,
        data.get("farmer_name", "Farmer"),
        data.get("village", "Local Village"),
        data.get("crop", "rice"),
        data.get("growth_stage", "vegetative"),
        data.get("disease_id"),
        data.get("disease_name"),
        data.get("confidence"),
        data.get("farm_risk_score"),
        data.get("risk_level"),
        data.get("temperature_c"),
        data.get("humidity_pct"),
        data.get("iot_trap_count"),
        data.get("latitude"),
        data.get("longitude"),
        data.get("expert_status", "AI-Flagged"),
        json.dumps(data.get("xai_breakdown", [])),
        json.dumps(data.get("advisory_payload", {})),
        now
    ))
    conn.commit()
    conn.close()
    return report_id

def get_all_reports() -> list:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports ORDER BY created_at DESC")
    rows = cursor.fetchall()
    
    result = []
    for r in rows:
        item = dict(r)
        item["xai_breakdown"] = json.loads(item["xai_breakdown"]) if item["xai_breakdown"] else []
        item["advisory_payload"] = json.loads(item["advisory_payload"]) if item["advisory_payload"] else {}
        result.append(item)
        
    conn.close()
    return result

def update_report_status(report_id: str, expert_status: str, adjusted_risk_level: str = None) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if adjusted_risk_level:
        cursor.execute("UPDATE reports SET expert_status = ?, risk_level = ? WHERE id = ?", (expert_status, adjusted_risk_level, report_id))
    else:
        cursor.execute("UPDATE reports SET expert_status = ? WHERE id = ?", (expert_status, report_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

def save_alert(data: dict) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    alert_id = f"ALT-{uuid.uuid4().hex[:6].upper()}"
    now = datetime.utcnow().isoformat()

    cursor.execute("""
    INSERT INTO alerts (id, target_village, radius_km, alert_title, message_hi, message_en, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        alert_id,
        data.get("target_village"),
        data.get("radius_km"),
        data.get("alert_title"),
        data.get("message_hi"),
        data.get("message_en"),
        now
    ))
    conn.commit()
    conn.close()
    return alert_id

def get_all_alerts() -> list:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY created_at DESC")
    rows = cursor.fetchall()
    result = [dict(r) for r in rows]
    conn.close()
    return result
