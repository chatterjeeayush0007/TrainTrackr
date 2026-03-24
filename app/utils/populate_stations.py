# app/utils/populate_stations.py
import json
from app.db.mongodb import db, stations_collection
from app.utils.locationiq_mapper import get_coords_from_pincode

# Load trains.json
with open("app/data/trains.json", "r", encoding="utf-8") as f:
    trains = json.load(f)

# Set to store unique stations
unique_stations = {}

for train in trains:
    for stop in train.get("stops", []):
        station_name = stop["station"]
        if station_name not in unique_stations:
            # Option 1: If you know pincode for each station, use it:
            # lat, lon = get_coords_from_pincode(station_pincode)

            # Option 2: If no pincode, you can pass station_name + city or just station_name
            lat, lon = get_coords_from_pincode(station_name)
            unique_stations[station_name] = {"name": station_name, "lat": lat, "lon": lon}

# Insert all unique stations into MongoDB
for station in unique_stations.values():
    # Avoid duplicates
    if stations_collection.find_one({"name": station["name"]}) is None:
        stations_collection.insert_one(station)

print(f"✅ Inserted {len(unique_stations)} stations into MongoDB.")