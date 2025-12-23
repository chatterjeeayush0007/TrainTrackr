import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

CROWD_SCORE = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

# -----------------------------
# API helpers
# -----------------------------
def get_trains():
    resp = requests.get(f"{BASE_URL}/trains/")
    resp.raise_for_status()
    return resp.json()["trains"]

def get_train_route(train_no):
    resp = requests.get(f"{BASE_URL}/trains/{train_no}/route")
    resp.raise_for_status()
    return resp.json()

def get_delay(train_no):
    resp = requests.get(f"{BASE_URL}/predictions/delay/{train_no}")
    resp.raise_for_status()
    return resp.json()["predicted_delay_minutes"]

def search_station(query):
    resp = requests.get(f"{BASE_URL}/stations/search", params={"q": query})
    resp.raise_for_status()
    return resp.json()["results"]

def get_crowd_level(station):
    resp = requests.get(f"{BASE_URL}/crowd/{station}")
    resp.raise_for_status()
    return resp.json()["crowd_level"]

# -----------------------------
# Core logic
# -----------------------------
def find_best_train(start_station, dest_station, arrival_time):
    arrival_dt = datetime.strptime(arrival_time, "%H:%M")
    trains = get_trains()
    candidates = []

    crowd = get_crowd_level(start_station)
    crowd_penalty = CROWD_SCORE.get(crowd, 1)

    for train in trains:
        route = get_train_route(train["train_no"])
        stops = route["stops"]

        start_index = next(
            (i for i, s in enumerate(stops)
             if s["station"].lower() == start_station.lower()), None)

        dest_index = next(
            (i for i, s in enumerate(stops)
             if s["station"].lower() == dest_station.lower()), None)

        if start_index is None or dest_index is None or start_index >= dest_index:
            continue

        delay = get_delay(train["train_no"])
        scheduled_arrival = datetime.strptime(
            stops[dest_index]["arrival"], "%H:%M"
        )
        expected_arrival = scheduled_arrival + timedelta(minutes=delay)

        time_diff = int((expected_arrival - arrival_dt).total_seconds() / 60)

        candidates.append({
            "train_no": train["train_no"],
            "train_name": train["train_name"],
            "expected_arrival": expected_arrival,
            "delay": delay,
            "time_diff": time_diff,
            "crowd": crowd,
            "crowd_penalty": crowd_penalty
        })

    if not candidates:
        return None, None

    on_time = [c for c in candidates if c["time_diff"] <= 0]

    if on_time:
        best = min(
            on_time,
            key=lambda x: (x["crowd_penalty"], abs(x["time_diff"]))
        )
        return best, "on_time"
    else:
        best = min(
            candidates,
            key=lambda x: (x["crowd_penalty"], x["time_diff"])
        )
        return best, "late"

# -----------------------------
# CLI
# -----------------------------
def main():
    print("\n🚆 Welcome to TrainTrackr\n")

    start_station = input("Enter your starting station: ").strip()
    dest_station = input("Enter your destination station: ").strip()
    arrival_time = input("Enter desired arrival time (HH:MM): ").strip()

    try:
        search_station(start_station)
        search_station(dest_station)
    except Exception:
        print("❌ Invalid station name.")
        return

    result, status = find_best_train(
        start_station, dest_station, arrival_time
    )

    if not result:
        print("\n❌ No trains found for this route.")
        return

    if status == "on_time":
        print("\n✅ You can reach on time!")
    else:
        print("\n⚠️ No train can reach by your desired time.")
        print("Showing the closest possible option.")

    print("\n📌 Recommended Train")
    print(f"Train No   : {result['train_no']}")
    print(f"Train Name : {result['train_name']}")
    print(f"Arrival    : {result['expected_arrival'].strftime('%H:%M')}")
    print(f"Delay      : {result['delay']} min")
    print(f"Crowd      : {result['crowd']}")

    if result["time_diff"] <= 0:
        print(f"🕒 Arrives {abs(result['time_diff'])} min early")
    else:
        print(f"🕒 Arrives {result['time_diff']} min late")

if __name__ == "__main__":
    main()
