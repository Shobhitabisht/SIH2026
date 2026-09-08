"""
Geospatial Sentinel-2 NDVI Vegetation Index Simulation Module
Provides regional crop health index (NDVI: Normalized Difference Vegetation Index) overlays.
"""

from typing import Dict, Any, List

class Sentinel2NDVIProcessor:
    
    @staticmethod
    def get_regional_ndvi(lat: float = 19.7515, lng: float = 75.7139) -> Dict[str, Any]:
        """
        Generates simulated Sentinel-2 NDVI grid features around the specified coordinates.
        NDVI ranges from -1.0 to +1.0:
         < 0.2: Bare soil / stressed vegetation
         0.2 - 0.5: Moderately stressed crop canopy (potential disease/pest outbreak)
         0.6 - 0.9: Healthy dense vegetation
        """
        features = []
        # Generate grid around region (e.g. Jalna / Aurangabad district, Maharashtra)
        delta_grid = [-0.04, -0.02, 0.0, 0.02, 0.04]
        
        for i, d_lat in enumerate(delta_grid):
            for j, d_lng in enumerate(delta_grid):
                grid_lat = round(lat + d_lat, 4)
                grid_lng = round(lng + d_lng, 4)
                
                # Introduce lower NDVI values in central region to simulate disease stress zone
                dist = (d_lat**2 + d_lng**2)**0.5
                if dist < 0.03:
                    ndvi_val = round(0.32 - (dist * 2), 2)
                    status = "Stressed - High Risk Spot"
                else:
                    ndvi_val = round(0.72 + (dist * 1.5), 2)
                    status = "Healthy Vegetation"

                ndvi_val = min(0.92, max(0.15, ndvi_val))

                polygon = [
                    [grid_lng - 0.008, grid_lat - 0.008],
                    [grid_lng + 0.008, grid_lat - 0.008],
                    [grid_lng + 0.008, grid_lat + 0.008],
                    [grid_lng - 0.008, grid_lat + 0.008],
                    [grid_lng - 0.008, grid_lat - 0.008]
                ]

                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [polygon]
                    },
                    "properties": {
                        "cell_id": f"GRID_{i}_{j}",
                        "ndvi_score": ndvi_val,
                        "health_status": status,
                        "satellite_source": "Sentinel-2 L2A (10m Res)"
                    }
                })

        return {
            "type": "FeatureCollection",
            "metadata": {
                "sensor": "Sentinel-2 MSI",
                "index": "NDVI (Normalized Difference Vegetation Index)",
                "region_center": [lat, lng]
            },
            "features": features
        }
