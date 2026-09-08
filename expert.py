"""
Expert Web Portal & Government Officer REST API Endpoints
"""

from fastapi import APIRouter, HTTPException
from backend.app.db.models import ExpertValidationRequest, BroadcastAlertRequest
from backend.app.db.database import get_all_reports, update_report_status, save_alert, get_all_alerts

router = APIRouter(prefix="/api/expert", tags=["Expert Web Portal Services"])

@router.get("/reports")
async def get_expert_dashboard_reports():
    """
    Returns list of all incoming farmer reports with AI risk scores, confidence values,
    and validation status for expert review.
    """
    reports = get_all_reports()
    return {
        "status": "success",
        "total_count": len(reports),
        "high_risk_count": sum(1 for r in reports if r.get("risk_level") == "High"),
        "pending_validation_count": sum(1 for r in reports if r.get("expert_status") == "AI-Flagged"),
        "reports": reports
    }

@router.post("/validate")
async def validate_report(req: ExpertValidationRequest):
    """
    Expert-in-the-loop endpoint: allows an agricultural officer to validate or override
    an AI risk score / flag to eliminate false alarms before broadcasting alerts.
    """
    success = update_report_status(
        report_id=req.report_id,
        expert_status=req.expert_status,
        adjusted_risk_level=req.adjusted_risk_level
    )
    if not success:
        raise HTTPException(status_code=404, detail="Report ID not found.")

    return {
        "status": "success",
        "message": f"Report {req.report_id} updated to '{req.expert_status}'.",
        "report_id": req.report_id,
        "expert_status": req.expert_status
    }

@router.post("/broadcast")
async def broadcast_alert(req: BroadcastAlertRequest):
    """
    Triggers a regional advisory SMS/Push broadcast to farmers in affected radius.
    """
    alert_id = save_alert({
        "target_village": req.target_village,
        "radius_km": req.radius_km,
        "alert_title": req.alert_title,
        "message_hi": req.message_hi,
        "message_en": req.message_en
    })

    return {
        "status": "success",
        "alert_id": alert_id,
        "broadcast_summary": f"Alert broadcasted to all registered farmers in {req.target_village} within {req.radius_km} km radius.",
        "alert_details": req
    }

@router.get("/alerts")
async def get_broadcast_alerts():
    """
    Returns log of all issued emergency outbreak alerts.
    """
    alerts = get_all_alerts()
    return {"status": "success", "alerts": alerts}
