"""
Geospatial API Endpoints (GeoJSON Hotspots & Sentinel-2 NDVI Layers)
"""

from fastapi import APIRouter
from backend.app.geospatial.hotspot import HotspotService
from backend.app.geospatial.ndvi import Sentinel2NDVIProcessor
from backend.app.db.database import get_all_reports

router = APIRouter(prefix="/api/geospatial", tags=["Geospatial Services"])

@router.get("/hotspots")
async def get_hotspot_geojson():
    """
    Returns live GeoJSON FeatureCollection of all flagged crop disease reports.
    """
    reports = get_all_reports()
    geojson_payload = HotspotService.generate_geojson_hotspots(reports)
    return geojson_payload

@router.get("/ndvi")
async def get_sentinel2_ndvi_layer(lat: float = 19.7515, lng: float = 75.7139):
    """
    Returns Sentinel-2 NDVI satellite vegetation index polygon grid around target coordinates.
    """
    ndvi_geojson = Sentinel2NDVIProcessor.get_regional_ndvi(lat=lat, lng=lng)
    return ndvi_geojson
