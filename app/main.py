from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI(
    title="TrainTrackr API",
    description="Backend for TrainTrackr local train utility app",
    version="1.0.0"
)

# -----------------------------
# Enable CORS for frontend
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
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
# Trains
try:
    from app.routes.trains import router as trains_router
    app.include_router(trains_router)
except ImportError as e:
    print("Trains route not loaded:", e)

# Stations
try:
    from app.routes.stations import router as stations_router
    app.include_router(stations_router)
except ImportError as e:
    print("Stations route not loaded:", e)

# Predictions
try:
    from app.routes.predictions import router as predictions_router
    app.include_router(predictions_router)
except ImportError as e:
    print("Predictions route not loaded:", e)

# Crowd
try:
    from app.routes.crowd import router as crowd_router
    app.include_router(crowd_router)
except ImportError as e:
    print("Crowd route not loaded:", e)

# Recommendations (new)
try:
    from app.routes.recommendations import router as recommendations_router
    app.include_router(recommendations_router)
except ImportError as e:
    print("Recommendations route not loaded:", e)

# -----------------------------
# Background simulator
# -----------------------------
from app.utils.simulate_trains import run_simulator_forever

@app.on_event("startup")
async def start_background_simulator():
    asyncio.create_task(run_simulator_forever(interval_seconds=60))
