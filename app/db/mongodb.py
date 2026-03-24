# app/db/mongodb.py
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# -----------------------------
# MongoDB Atlas connection URI
# -----------------------------
uri = "mongodb+srv://traintrackr_user:traintrackr_205007@traintrackrcluster.1ljtogk.mongodb.net/?appName=TrainTrackrCluster"

# Create a MongoClient with server API version 1
client = MongoClient(uri, server_api=ServerApi('1'))

# Select the database
db = client["traintrackr_db"]

# -----------------------------
# Collections
# -----------------------------
users_collection = db["users"]
trains_collection = db["trains"]
crowd_collection = db["crowd_data"]
stations_collection = db["stations"]  # <-- added for GPS mapping

# -----------------------------
# Test the connection
# -----------------------------
try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print(f"❌ Connection failed: {e}")