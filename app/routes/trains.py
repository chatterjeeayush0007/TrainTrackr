# app/routes/trains.py

from fastapi import APIRouter, HTTPException 
import json
from pathlib import Path
from app.utils.crowd_predict import CrowdPredictor

# Initialize crowd predictor (bypassing MongoDB for the demo)
crowd_predictor = CrowdPredictor(None)

# Removed the prefix="/trains" here because it is already handled in main.py
router = APIRouter(tags=["Trains"])

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "trains.json"

def load_trains():
    """Load current trains.json and extract all trains from their time slots"""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        all_trains = []
        # trains.json is a list of time slots, so we need to loop through them
        for slot_data in raw_data:
            if "trains" in slot_data:
                # Add all trains from this slot into our master list
                all_trains.extend(slot_data["trains"])
                
        return all_trains

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="trains.json not found")

def get_crowd_level(user_count: int):
    """Convert user count to Low/Medium/High"""
    if user_count < 50:
        return "Low"
    elif user_count < 150:
        return "Medium"
    else:
        return "High"

@router.get("/")
def get_all_trains():
    """
    Returns basic info of all trains with optional crowd level
    """
    data = load_trains()
    trains = []

    for train in data:
        current_station = train.get("current_station")
        delay = train.get("delay", 0)
        
        # Safely get the train number, default to 0 if missing
        train_no = train.get("train_no", 0) 
        
        user_count = crowd_predictor.predict_crowd_for_train(train_no)
        crowd_level = get_crowd_level(user_count)

        trains.append({
            "train_no": train_no,
            "train_name": train.get("train_name"),
            "current_station": current_station,
            "delay": delay,
            "crowd_level": crowd_level
        })

    return {
        "count": len(trains),
        "trains": trains
    }

@router.get("/{train_no}")
def get_train_by_number(train_no: int):
    """
    Returns full details of a specific train, including live status, expected times, and crowd level
    """
    data = load_trains()
    train = next((t for t in data if t.get("train_no") == train_no), None)

    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    current_station = train.get("current_station")
    delay = train.get("delay", 0)

    # Predict crowd level at current station
    user_count = crowd_predictor.predict_crowd_for_train(train_no)
    crowd_level = get_crowd_level(user_count)

    # Build route with expected arrival/departure times
    route = []
    for stop in train.get("stops", []):
        route.append({
            "station": stop.get("station"),
            "scheduled_arrival": stop.get("arrival"),
            "scheduled_departure": stop.get("departure"),
            "expected_arrival": train.get("expected_arrival") if stop.get("station") == current_station else stop.get("arrival"),
            "expected_departure": train.get("expected_departure") if stop.get("station") == current_station else stop.get("departure")
        })

    return {
        "train_no": train_no,
        "train_name": train.get("train_name"),
        "current_station": current_station,
        "delay_minutes": delay,
        "crowd_level": crowd_level,
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