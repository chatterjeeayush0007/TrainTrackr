# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(
    title="TrainTrackr API",
    description="Backend for TrainTrackr local train utility app",
    version="1.0.0"
)

# -----------------------------
# Enable CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Root / Health check
# -----------------------------
@app.get("/")
def root():
    return {
        "status": "running",
        "project": "TrainTrackr"
    }

# -----------------------------
# Include routers
# -----------------------------
from app.routes import trains, stations, predictions, recommendations, users, railradar

# Trains
app.include_router(trains.router)

# Stations
app.include_router(stations.router)

# Predictions
app.include_router(predictions.router)

# Recommendations
app.include_router(recommendations.router)

# Users
app.include_router(users.router)

# RailRadar
app.include_router(railradar.router, prefix="/railradar", tags=["RailRadar"])

# -----------------------------
# Background simulator
# -----------------------------
from app.utils.simulate_trains import run_simulator_forever

@app.on_event("startup")
async def start_background_simulator():
    asyncio.create_task(run_simulator_forever(interval_seconds=60))