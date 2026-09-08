"""
Geospatial Hotspot Mapping Service & Village Alert Dispatcher
Generates GeoJSON points and clusters for high-risk crop disease cases,
and evaluates proximity thresholds to alert nearby agricultural experts and farmers.
"""

import math
from typing import List, Dict, Any

class HotspotService:

    @staticmethod
    def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Haversine formula to compute distance in kilometers between 2 coordinates."""
        R = 6371.0 # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 2)

    @classmethod
    def generate_geojson_hotspots(cls, reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Transforms farmer diagnosis reports into a GeoJSON FeatureCollection with risk styling.
        """
        features = []
        for r in reports:
            risk_level = r.get("risk_level", "Low")
            color = "#DC2626" if risk_level == "High" else ("#D97706" if risk_level == "Medium" else "#16A34A")

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [r.get("longitude", 75.7139), r.get("latitude", 19.7515)]
                },
                "properties": {
                    "report_id": r.get("id"),
                    "farmer_name": r.get("farmer_name", "Local Farmer"),
                    "village": r.get("village", "Jalna Central"),
                    "crop": r.get("crop", "Rice"),
                    "disease_name": r.get("disease_name", "Rice Blast"),
                    "risk_score": r.get("farm_risk_score", 0.85),
                    "risk_level": risk_level,
                    "color": color,
                    "status": r.get("expert_status", "AI-Flagged"),
                    "created_at": r.get("created_at", "2026-09-05T20:00:00Z")
                }
            }
            features.append(feature)

        return {
            "type": "FeatureCollection",
            "features": features
        }

    @classmethod
    def check_nearby_alerts(cls, new_lat: float, new_lng: float, risk_level: str, reports: List[Dict[str, Any]], radius_km: float = 10.0) -> Dict[str, Any]:
        """
        Checks if a high-risk case triggers a regional outbreak warning for nearby villages.
        """
        if risk_level != "High":
            return {"alert_triggered": False, "nearby_cases_count": 0, "affected_villages": []}

        nearby_count = 0
        affected_villages = set()

        for r in reports:
            dist = cls.calculate_distance_km(new_lat, new_lng, r.get("latitude", 0), r.get("longitude", 0))
            if dist <= radius_km and r.get("risk_level") == "High":
                nearby_count += 1
                if "village" in r:
                    affected_villages.add(r["village"])

        alert_triggered = nearby_count >= 2 # Trigger outbreak alert if 2+ high-risk cases in radius

        return {
            "alert_triggered": alert_triggered,
            "nearby_cases_count": nearby_count,
            "radius_km": radius_km,
            "affected_villages": list(affected_villages),
            "alert_message": f"WARNING: Outbreak cluster detected! {nearby_count} high-risk cases within {radius_km} km radius." if alert_triggered else "Single isolated high-risk report recorded."
        }
