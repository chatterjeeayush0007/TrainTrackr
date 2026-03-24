# app/routes/predictions.py

from fastapi import APIRouter, HTTPException  # pyright: ignore[reportMissingImports]
from datetime import datetime, timedelta
import json
from pathlib import Path
from app.utils.delay_predict import predict_delay
from app.utils.crowd_predict import CrowdPredictor
from app.db.mongodb import users_collection

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
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


@router.get("/delay/{train_no}")
def delay_prediction(train_no: int):
    """
    Return live delay, current station, expected arrival/departure for a train
    Falls back to heuristic predict_delay() if delay not available
    """
    trains = load_trains()
    train_data = next((t for t in trains if t.get("train_no") == train_no), None)

    if not train_data:
        raise HTTPException(status_code=404, detail="Train not found")

    # Live delay from JSON or fallback
    delay_minutes = train_data.get("delay")
    if delay_minutes is None:
        delay_minutes = predict_delay(train_no)

    status = "On Time" if delay_minutes <= 5 else "Delayed"

    # Current station
    current_station = train_data.get("current_station")

    # Expected arrival/departure
    expected_arrival = train_data.get("expected_arrival")
    expected_departure = train_data.get("expected_departure")

    # Optional: If expected times missing, calculate from now + delay
    if not expected_arrival:
        expected_arrival = (datetime.now() + timedelta(minutes=delay_minutes)).strftime("%H:%M")
    if not expected_departure:
        expected_departure = (datetime.now() + timedelta(minutes=delay_minutes + 5)).strftime("%H:%M")

    # Crowd prediction using CrowdPredictor
    predictor = CrowdPredictor(users_collection)
    predicted_crowd = predictor.predict_crowd_for_train(train_no)

    return {
        "train_no": train_no,
        "train_name": train_data.get("train_name"),
        "current_station": current_station,
        "predicted_delay_minutes": delay_minutes,
        "status": status,
        "expected_arrival": expected_arrival,
        "expected_departure": expected_departure,
        "predicted_crowd": predicted_crowd
    }


@router.get("/all")
def all_trains_with_crowd():
    """
    Return all trains with predicted delay and estimated crowd
    Useful for dashboard
    """
    trains = load_trains()
    predictor = CrowdPredictor(users_collection)
    results = []

    for t in trains:
        train_no = t.get("train_no")
        delay_minutes = t.get("delay") or predict_delay(train_no)
        status = "On Time" if delay_minutes <= 5 else "Delayed"
        expected_arrival = t.get("expected_arrival") or (datetime.now() + timedelta(minutes=delay_minutes)).strftime("%H:%M")
        expected_departure = t.get("expected_departure") or (datetime.now() + timedelta(minutes=delay_minutes + 5)).strftime("%H:%M")
        predicted_crowd = predictor.predict_crowd_for_train(train_no)

        results.append({
            "train_no": train_no,
            "train_name": t.get("train_name"),
            "current_station": t.get("current_station"),
            "predicted_delay_minutes": delay_minutes,
            "status": status,
            "expected_arrival": expected_arrival,
            "expected_departure": expected_departure,
            "predicted_crowd": predicted_crowd
        })

    return {"trains": results}