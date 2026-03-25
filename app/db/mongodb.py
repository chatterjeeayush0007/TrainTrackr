from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# -----------------------------
# MongoDB URI (SECURE)
# -----------------------------
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
trains_collection = db["trains"]
crowd_collection = db["crowd_data"]
stations_collection = db["stations"]

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


# Run test only when file is executed directly
if __name__ == "__main__":
    test_connection()