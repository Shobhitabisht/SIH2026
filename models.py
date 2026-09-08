"""
Pydantic Data Schemas & SQLite Database Models
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DiagnoseRequest(BaseModel):
    farmer_name: str = "Ramesh Kumar"
    village: str = "Ambad Village"
    crop: str = "rice"
    growth_stage: str = "vegetative"
    temperature_c: float = 29.0
    humidity_pct: float = 84.0
    iot_trap_count: int = 48
    latitude: float = 19.7515
    longitude: float = 75.7139
    language: str = "hi"

class ExpertValidationRequest(BaseModel):
    report_id: str
    expert_status: str # "Verified - Confirmed" | "Overridden - False Alarm" | "Pending Field Visit"
    expert_notes: Optional[str] = "Confirmed via expert visual analysis."
    adjusted_risk_level: Optional[str] = None

class BroadcastAlertRequest(BaseModel):
    target_village: str
    radius_km: float = 15.0
    alert_title: str = "High Pest Outbreak Warning"
    message_hi: str = "चेतावनी: आपके क्षेत्र में धान का झुलसा रोग तेजी से फैल रहा है। तुरंत स्प्रे करें।"
    message_en: str = "ALERT: Rice blast outbreak detected in your 15km zone. Apply preventive spray."
