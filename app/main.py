# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# 1️⃣ ADDED 'trains' to the imports here:
from app.routes import users, stations, trains

app = FastAPI(title="TrainTrackr API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {"status": "running", "project": "TrainTrackr"}

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])  
app.include_router(stations.router, prefix="/stations", tags=["Stations"])
# 2️⃣ ADDED the trains router here:
app.include_router(trains.router, prefix="/trains", tags=["Trains"])

# Background simulator
from app.utils.simulate_trains import run_simulator_forever

@app.on_event("startup")
async def start_background_simulator():
    asyncio.create_task(run_simulator_forever(interval_seconds=60))