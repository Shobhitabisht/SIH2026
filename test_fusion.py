"""
Unit tests for Weather & Risk Fusion Engine
"""

import pytest
from backend.app.engine.risk_fusion import RiskFusionEngine

def test_risk_fusion_high_risk():
    result = RiskFusionEngine.calculate_risk(
        disease_id="rice_blast",
        ai_confidence=0.92,
        temperature_c=29.0,
        humidity_pct=88.0,
        growth_stage="vegetative",
        iot_trap_count=60
    )
    assert result["farm_risk_score"] >= 0.70
    assert result["risk_level"] == "High"
    assert len(result["xai_breakdown"]) == 4

def test_risk_fusion_healthy():
    result = RiskFusionEngine.calculate_risk(
        disease_id="healthy",
        ai_confidence=0.95,
        temperature_c=25.0,
        humidity_pct=55.0,
        growth_stage="vegetative",
        iot_trap_count=10
    )
    assert result["farm_risk_score"] < 0.40
    assert result["risk_level"] == "Low"
