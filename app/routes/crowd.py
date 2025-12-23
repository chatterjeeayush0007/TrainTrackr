from fastapi import APIRouter, HTTPException
from datetime import datetime
import json
from pathlib import Path

router = APIRouter(
    prefix="/crowd",
    tags=["Crowd Estimation"]
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "trains.json"


def load_trains():
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="trains.json not found")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise HTTPException(status_code=500, detail="Invalid trains data format")

    return data


@router.get("/{station}")
def estimate_crowd(station: str):
    """
    Estimate crowd at a station based on train frequency and time of day
    """
    trains = load_trains()
    hour = datetime.now().hour

    count = 0
    for train in trains:
        for stop in train.get("stops", []):
            if stop.get("station", "").lower() == station.lower():
                count += 1

    if count == 0:
        raise HTTPException(status_code=404, detail="Station not found")

    is_peak = (7 <= hour <= 10) or (17 <= hour <= 20)

    if is_peak:
        level = "High" if count >= 2 else "Medium"
    else:
        level = "Medium" if count >= 1 else "Low"

    return {
        "station": station,
        "current_hour": hour,
        "train_count": count,
        "crowd_level": level
    }
