from datetime import datetime, timedelta
from app.routes.trains import load_trains
from app.routes.predictions import predict_delay

CROWD_SCORE = {"Low": 0, "Medium": 1, "High": 2}

def find_best_train_backend(start_station: str, dest_station: str, arrival_time: str):
    arrival_dt = datetime.strptime(arrival_time, "%H:%M")
    trains = load_trains()  # full train data
    candidates = []

    # Estimate crowd level at start station
    crowd_count = sum(
        1 for train in trains for stop in train.get("stops", [])
        if stop["station"].lower() == start_station.lower()
    )

    hour = datetime.now().hour
    is_peak = (7 <= hour <= 10) or (17 <= hour <= 20)
    if is_peak:
        crowd_level = "High" if crowd_count >= 2 else "Medium"
    else:
        crowd_level = "Medium" if crowd_count >= 1 else "Low"

    crowd_penalty = CROWD_SCORE.get(crowd_level, 1)

    for train in trains:
        stops = train.get("stops", [])
        start_index = next((i for i, s in enumerate(stops)
                            if s["station"].lower() == start_station.lower()), None)
        dest_index = next((i for i, s in enumerate(stops)
                           if s["station"].lower() == dest_station.lower()), None)

        if start_index is None or dest_index is None or start_index >= dest_index:
            continue

        delay = train.get("delay")
        if delay is None:
            delay = predict_delay(train["train_no"])

        scheduled_arrival = datetime.strptime(stops[dest_index]["arrival"], "%H:%M")
        expected_arrival = scheduled_arrival + timedelta(minutes=delay)
        time_diff = int((expected_arrival - arrival_dt).total_seconds() / 60)

        candidates.append({
            "train_no": train["train_no"],
            "train_name": train["train_name"],
            "expected_arrival": expected_arrival,
            "delay": delay,
            "time_diff": time_diff,
            "crowd": crowd_level,
            "crowd_penalty": crowd_penalty
        })

    if not candidates:
        return None, None

    on_time = [c for c in candidates if c["time_diff"] <= 0]

    if on_time:
        best = min(on_time, key=lambda x: (x["crowd_penalty"], abs(x["time_diff"])))
        return best, "on_time"
    else:
        best = min(candidates, key=lambda x: (x["crowd_penalty"], x["time_diff"]))
        return best, "late"
