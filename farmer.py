"""
Farmer REST API Endpoints (Photo Upload, AI Diagnosis, Offline Sync)
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import json

from backend.app.ai.classifier import classifier
from backend.app.engine.risk_fusion import RiskFusionEngine
from backend.app.engine.advisory import AdvisoryEngine
from backend.app.geospatial.hotspot import HotspotService
from backend.app.db.database import save_report, get_all_reports

router = APIRouter(prefix="/api/farmer", tags=["Farmer PWA Services"])

@router.post("/diagnose")
async def diagnose_crop(
    image: Optional[UploadFile] = File(None),
    farmer_name: str = Form("Ramesh Kumar"),
    village: str = Form("Jalna Central"),
    crop: str = Form("rice"),
    growth_stage: str = Form("vegetative"),
    temperature_c: float = Form(29.5),
    humidity_pct: float = Form(86.0),
    iot_trap_count: int = Form(48),
    latitude: float = Form(19.7515),
    longitude: float = Form(75.7139),
    language: str = Form("hi")
):
    """
    Receives farmer photo upload + crop/location metadata, executes AI classification,
    fuses weather & pest signals into Farm Risk Score, and returns multilingual advisory.
    """
    # 1. Image AI Classification
    image_bytes = b""
    if image:
        image_bytes = await image.read()
    
    ai_result = classifier.predict(image_bytes, crop_hint=crop)
    disease_id = ai_result["disease_id"]
    confidence = ai_result["confidence"]

    # 2. Weather & Risk Fusion Calculation
    fusion_result = RiskFusionEngine.calculate_risk(
        disease_id=disease_id,
        ai_confidence=confidence,
        temperature_c=temperature_c,
        humidity_pct=humidity_pct,
        growth_stage=growth_stage,
        iot_trap_count=iot_trap_count
    )

    # 3. Multilingual Advisory Generation
    advisory_result = AdvisoryEngine.generate_advisory(disease_id=disease_id, lang=language)

    # 4. Save report & Check nearby hotspot outbreak threshold
    all_existing = get_all_reports()
    
    report_data = {
        "farmer_name": farmer_name,
        "village": village,
        "crop": crop,
        "growth_stage": growth_stage,
        "disease_id": disease_id,
        "disease_name": advisory_result["disease_name"],
        "confidence": confidence,
        "farm_risk_score": fusion_result["farm_risk_score"],
        "risk_level": fusion_result["risk_level"],
        "temperature_c": temperature_c,
        "humidity_pct": humidity_pct,
        "iot_trap_count": iot_trap_count,
        "latitude": latitude,
        "longitude": longitude,
        "expert_status": "AI-Flagged",
        "xai_breakdown": fusion_result["xai_breakdown"],
        "advisory_payload": advisory_result
    }

    report_id = save_report(report_data)

    outbreak_check = HotspotService.check_nearby_alerts(
        new_lat=latitude,
        new_lng=longitude,
        risk_level=fusion_result["risk_level"],
        reports=all_existing,
        radius_km=10.0
    )

    return {
        "status": "success",
        "report_id": report_id,
        "ai_prediction": {
            "disease_id": disease_id,
            "disease_name": advisory_result["disease_name"],
            "confidence": confidence,
            "model_architecture": ai_result["model_used"]
        },
        "risk_fusion": fusion_result,
        "advisory": advisory_result,
        "outbreak_warning": outbreak_check
    }

@router.post("/sync")
async def sync_offline_reports(reports_payload: str = Form(...)):
    """
    Offline PWA endpoint: processes batch queue of cached offline farmer uploads.
    """
    try:
        reports_list = json.loads(reports_payload)
        synced_ids = []
        for item in reports_list:
            disease_id = item.get("disease_id", "rice_blast")
            confidence = item.get("confidence", 0.85)
            
            fusion_result = RiskFusionEngine.calculate_risk(
                disease_id=disease_id,
                ai_confidence=confidence,
                temperature_c=item.get("temperature_c", 28.0),
                humidity_pct=item.get("humidity_pct", 80.0),
                growth_stage=item.get("growth_stage", "vegetative"),
                iot_trap_count=item.get("iot_trap_count", 30)
            )
            
            advisory_result = AdvisoryEngine.generate_advisory(disease_id=disease_id, lang=item.get("language", "hi"))

            item_data = {
                "farmer_name": item.get("farmer_name", "Offline Farmer"),
                "village": item.get("village", "Synced Village"),
                "crop": item.get("crop", "rice"),
                "growth_stage": item.get("growth_stage", "vegetative"),
                "disease_id": disease_id,
                "disease_name": advisory_result["disease_name"],
                "confidence": confidence,
                "farm_risk_score": fusion_result["farm_risk_score"],
                "risk_level": fusion_result["risk_level"],
                "temperature_c": item.get("temperature_c", 28.0),
                "humidity_pct": item.get("humidity_pct", 80.0),
                "iot_trap_count": item.get("iot_trap_count", 30),
                "latitude": item.get("latitude", 19.7515),
                "longitude": item.get("longitude", 75.7139),
                "expert_status": "AI-Flagged",
                "xai_breakdown": fusion_result["xai_breakdown"],
                "advisory_payload": advisory_result
            }
            rid = save_report(item_data)
            synced_ids.append(rid)

        return {"status": "success", "synced_count": len(synced_ids), "synced_ids": synced_ids}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Sync failed: {str(e)}")
