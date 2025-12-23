from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter(
    prefix="/trains",
    tags=["Trains"]
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "trains.json"


def load_trains():
    """Load current trains.json"""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="trains.json not found")
    return data


@router.get("/")
def get_all_trains():
    """
    Returns basic info of all trains
    """
    data = load_trains()
    trains = [
        {
            "train_no": train.get("train_no"),
            "train_name": train.get("train_name")
        }
        for train in data
    ]
    return {
        "count": len(trains),
        "trains": trains
    }


@router.get("/{train_no}")
def get_train_by_number(train_no: int):
    """
    Returns full details of a specific train, including live status and expected times
    """
    data = load_trains()
    train = next((t for t in data if t.get("train_no") == train_no), None)

    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    # Include current station and delay
    current_station = train.get("current_station")
    delay = train.get("delay", 0)

    # Build route with expected arrival/departure times
    route = []
    for stop in train.get("stops", []):
        route.append({
            "station": stop.get("station"),
            "scheduled_arrival": stop.get("arrival"),
            "scheduled_departure": stop.get("departure"),
            # If this is current station, show expected times from JSON
            "expected_arrival": train.get("expected_arrival") if stop.get("station") == current_station else stop.get("arrival"),
            "expected_departure": train.get("expected_departure") if stop.get("station") == current_station else stop.get("departure")
        })

    return {
        "train_no": train_no,
        "train_name": train.get("train_name"),
        "current_station": current_station,
        "delay_minutes": delay,
        "route": route
    }


@router.get("/{train_no}/route")
def get_train_route(train_no: int):
    """
    Returns route (stops) of a train without extra details
    """
    data = load_trains()
    train = next((t for t in data if t.get("train_no") == train_no), None)

    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    return {
        "train_no": train_no,
        "train_name": train.get("train_name"),
        "stops": train.get("stops", [])
    }
