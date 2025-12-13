from fastapi import APIRouter, HTTPException
from datetime import datetime
import json
from pathlib import Path

router = APIRouter(
    prefix="/crowd",
    tags=["Crowd Estimation"]
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "trains.json"

@router.get("/{station}")
def estimate_crowd(station: str):
    """
    Estimate crowd at a station based on train arrivals
    """
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="trains.json not found")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        trains = json.load(f)

    now = datetime.now()
    hour = now.hour

    # Count trains stopping at this station in peak vs off-peak
    count = 0
    for train in trains:
        for stop in train.get("stops", []):
            if stop.get("station", "").lower() == station.lower():
                count += 1

    # Simple logic: more trains = more crowd
    if 7 <= hour <= 10 or 17 <= hour <= 20:
        level = "High" if count >= 2 else "Medium"
    else:
        level = "Medium" if count >= 1 else "Low"

    return {
        "station": station,
        "current_hour": hour,
        "train_count": count,
        "crowd_level": level
    }
