"""
Integration tests for FastAPI endpoints
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_farmer_diagnose_endpoint():
    data = {
        "farmer_name": "Test Farmer",
        "village": "Test Village",
        "crop": "rice",
        "growth_stage": "vegetative",
        "temperature_c": "28.0",
        "humidity_pct": "85.0",
        "iot_trap_count": "45",
        "latitude": "19.7515",
        "longitude": "75.7139",
        "language": "hi"
    }
    response = client.post("/api/farmer/diagnose", data=data)
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "success"
    assert "report_id" in res
    assert "risk_fusion" in res
    assert "advisory" in res

def test_expert_reports_endpoint():
    response = client.get("/api/expert/reports")
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "success"
    assert "reports" in res

def test_geospatial_hotspots_endpoint():
    response = client.get("/api/geospatial/hotspots")
    assert response.status_code == 200
    res = response.json()
    assert res["type"] == "FeatureCollection"
