import json
import random
from pathlib import Path
from datetime import datetime, timedelta
import asyncio

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "trains.json"

def parse_time(time_str):
    """Parse HH:MM string to datetime today"""
    now = datetime.now()
    hour, minute = map(int, time_str.split(":"))
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)

def format_time(dt):
    return dt.strftime("%H:%M")

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

        # Initialize current_index if missing
        if "current_index" not in train:
            train["current_index"] = 0

        # Move to next stop (circular)
        train["current_index"] = (train["current_index"] + 1) % len(stops)
        current_stop = stops[train["current_index"]]
        train["current_station"] = current_stop["station"]

        # Random delay (-2 to +10 minutes)
        train["delay"] = random.randint(-2, 10)

        # Calculate expected arrival/departure using scheduled times + delay
        scheduled_arrival = parse_time(current_stop["arrival"])
        scheduled_departure = parse_time(current_stop["departure"])
        train["expected_arrival"] = format_time(scheduled_arrival + timedelta(minutes=train["delay"]))
        train["expected_departure"] = format_time(scheduled_departure + timedelta(minutes=train["delay"]))

    # Save updated trains.json
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(trains, f, indent=2)

    print("Trains.json updated with sequential live data and expected times")

async def run_simulator_forever(interval_seconds=60):
    while True:
        simulate_live_trains()
        await asyncio.sleep(interval_seconds)

if __name__ == "__main__":
    asyncio.run(run_simulator_forever(interval_seconds=10))  # fast demo
