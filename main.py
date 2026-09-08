"""
TerraSync FastAPI Main Application Entrypoint
SIH Problem Statement ID: SIH26131
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from backend.app.db.database import init_db
from backend.app.api.farmer import router as farmer_router
from backend.app.api.expert import router as expert_router
from backend.app.api.geospatial import router as geospatial_router

# Initialize SQLite database and seed records on startup
init_db()

app = FastAPI(
    title="TerraSync - AI Crop Disease & Pest Early Warning API",
    description="SIH26131 Hackathon Platform combining CNN AI, Weather/Risk Fusion, Geospatial Hotspots & PWA Advisory",
    version="1.0.0"
)

# CORS middleware enabling local and cross-origin access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(farmer_router)
app.include_router(expert_router)
app.include_router(geospatial_router)

# Mount Static Files directory for Web Frontend
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({
        "system": "TerraSync AI Platform",
        "status": "Online",
        "documentation": "/docs"
    })

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "TerraSync Backend"}
