# app/utils/simulate_trains.py

import json
import random
from pathlib import Path
from datetime import datetime, timedelta
import asyncio
from app.utils.crowd_predict import CrowdPredictor
from app.db.mongodb import get_users_collection  # your MongoDB helper

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "trains.json"

# Initialize crowd predictor
users_collection = get_users_collection()
crowd_predictor = CrowdPredictor(users_collection)


def parse_time(time_str):
    """Parse HH:MM string to datetime today. Defaults to 00:00 if missing."""
    now = datetime.now()
    if not time_str or not isinstance(time_str, str):
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        hour, minute = map(int, time_str.split(":"))
        return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    except ValueError:
        return now.replace(hour=0, minute=0, second=0, microsecond=0)


def format_time(dt):
    return dt.strftime("%H:%M")


def get_crowd_percentage(train_no):
    """Return crowd as percentage (0-100)"""
    users = crowd_predictor.predict_crowd_for_train(train_no)
    # Assume max capacity 200 passengers per train (mock)
    max_capacity = 200
    percentage = min(int((users / max_capacity) * 100), 100)
    return percentage


def simulate_live_trains():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            trains = json.load(f)
    except FileNotFoundError:
        print("trains.json not found")
        return

    for train in trains:
        stops = train.get("stops", [])
        if not stops:
            continue

        # Move to next stop (circular)
        if "current_index" not in train:
            train["current_index"] = 0
        train["current_index"] = (train["current_index"] + 1) % len(stops)

        current_stop = stops[train["current_index"]]
        train["current_station"] = current_stop.get("station", "Unknown")

        # Random delay (-2 to +10 minutes)
        train["delay"] = random.randint(-2, 10)

        # Calculate expected arrival/departure using scheduled times + delay
        scheduled_arrival = parse_time(current_stop.get("arrival"))
        scheduled_departure = parse_time(current_stop.get("departure"))
        train["expected_arrival"] = format_time(scheduled_arrival + timedelta(minutes=train["delay"]))
        train["expected_departure"] = format_time(scheduled_departure + timedelta(minutes=train["delay"]))

        # Calculate crowd percentage
        train["crowd_percentage"] = get_crowd_percentage(train.get("train_no"))

    # Save updated trains.json
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(trains, f, indent=2)

    print("Trains.json updated with live data, delays, and crowd percentages")


async def run_simulator_forever(interval_seconds=60):
    while True:
        simulate_live_trains()
        await asyncio.sleep(interval_seconds)


if __name__ == "__main__":
    # fast demo for testing
    asyncio.run(run_simulator_forever(interval_seconds=10))