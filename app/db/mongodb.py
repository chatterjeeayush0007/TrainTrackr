from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise Exception("❌ MONGODB_URI not found in environment variables. Please set it in .env file.")

# -----------------------------
# Create MongoDB Client
# -----------------------------
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

# -----------------------------
# Select Database
# -----------------------------
db = client["traintrackr_db"]

# -----------------------------
# Collections
# -----------------------------
users_collection = db["users"]
trains_collection = db["trips"]
crowd_collection = db["crowd_predictions"]
stations_collection = db["stations"]
population_collection = db["population_data"]

# -----------------------------
# Test Connection
# -----------------------------
def test_connection():
    try:
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

# -----------------------------
# Reset collections (delete all data)
# -----------------------------
def reset_collections():
    try:
        trains_collection.delete_many({})
        stations_collection.delete_many({})
        population_collection.delete_many({})
        crowd_collection.delete_many({})
        users_collection.delete_many({})
        print("🗑️ All mock collections cleared!")
    except Exception as e:
        print(f"❌ Failed to reset collections: {e}")

# -----------------------------
# Load mock JSON data into MongoDB
# -----------------------------
def load_mock_data():
    # Load train data
    trains_data = []
    try:
        with open("app/data/trains.json", "r", encoding="utf-8") as f:
            trains_data = json.load(f)
        if trains_data:
            trains_collection.insert_many(trains_data)
            print(f"✅ Inserted {len(trains_data)} trains into 'trips' collection")
        else:
            print("⚠️ No trains data to insert")
    except Exception as e:
        print(f"❌ Failed to insert trains data: {e}")

    # Load pincode population data
    try:
        with open("app/data/pincode_population.json", "r", encoding="utf-8") as f:
            population_data = json.load(f)
        population_docs = [{"pincode": k, **v} for k, v in population_data.items()]
        if population_docs:
            population_collection.insert_many(population_docs)
            print(f"✅ Inserted {len(population_docs)} entries into 'population_data' collection")
        else:
            print("⚠️ No population data to insert")
    except Exception as e:
        print(f"❌ Failed to insert population data: {e}")

    # Extract and insert unique stations
    try:
        if trains_data:
            all_stations = {}
            for train in trains_data:
                for stop in train.get("stops", []):
                    name = stop.get("station")
                    if not name:
                        continue
                    if name not in all_stations:
                        all_stations[name] = {"station_name": name, "trains": [train["train_no"]]}
                    else:
                        all_stations[name]["trains"].append(train["train_no"])
            station_docs = list(all_stations.values())
            if station_docs:
                stations_collection.insert_many(station_docs)
                print(f"✅ Inserted {len(station_docs)} unique stations into 'stations' collection")
            else:
                print("⚠️ No stations data to insert")
    except Exception as e:
        print(f"❌ Failed to insert stations data: {e}")

    # Load mock users
    try:
        with open("app/data/users.json", "r", encoding="utf-8") as f:
            users_data = json.load(f)
        if users_data:
            users_collection.insert_many(users_data)
            print(f"✅ Inserted {len(users_data)} users into 'users' collection")
        else:
            print("⚠️ No users data to insert")
    except Exception as e:
        print(f"❌ Failed to insert users data: {e}")

# -----------------------------
# Generate realistic mock crowd predictions
# -----------------------------
def generate_mock_crowd():
    try:
        # Build population lookup by pincode
        pop_data = {doc["pincode"]: doc["population"] for doc in population_collection.find({})}
        if not pop_data:
            print("⚠️ No population data available, skipping crowd generation")
            return

        crowd_docs = []

        for train in trains_collection.find({}):
            current_index = train.get("current_index", 0)
            stops = train.get("stops", [])
            if not stops or current_index >= len(stops):
                continue

            current_station = stops[current_index].get("station")
            if not current_station:
                continue

            # Find population for this station: sum first 5 nearby pincodes for mock realism
            nearby_pincodes = list(pop_data.keys())[:5]
            population_sum = sum(pop_data[p] for p in nearby_pincodes)
            delay_factor = train.get("delay", 0) * 10
            predicted_crowd = max(0, int(population_sum * 0.001 + delay_factor))

            crowd_docs.append({
                "train_no": train["train_no"],
                "station": current_station,
                "predicted_crowd": predicted_crowd,
                "timestamp": datetime.now().isoformat()
            })

        if crowd_docs:
            crowd_collection.insert_many(crowd_docs)
            print(f"✅ Inserted {len(crowd_docs)} mock crowd predictions")
        else:
            print("⚠️ No crowd predictions to insert")
    except Exception as e:
        print(f"❌ Failed to generate mock crowd predictions: {e}")

# -----------------------------
# Run everything
# -----------------------------
if __name__ == "__main__":
    if test_connection():
        reset_collections()      # Clear old data before inserting
        load_mock_data()         # Insert mock trains, stations, population, users
        generate_mock_crowd()    # Generate mock crowd predictions