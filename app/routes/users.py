from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from app.db.mongodb import users_collection, stations_collection
from app.utils.crowd_predict import CrowdPredictor
from app.utils.locationiq_mapper import get_coords_from_pincode
from math import radians, cos, sin, asin, sqrt

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# -----------------------------
# Pydantic schema for user input
# -----------------------------
class UserDetails(BaseModel):
    username: str = Field(..., description="Unique username or email")
    pincode: str = Field(..., description="User's area pincode")
    passenger_type: str = Field(..., description="daily or occasional")
    ticket_type: str = Field(..., description="single, monthly, etc.")
    from_date: Optional[date] = Field(None, description="For monthly tickets: start date")
    to_date: Optional[date] = Field(None, description="For monthly tickets: end date")
    journey_time: str = Field(..., description="Time of travel in HH:MM format")
    source_station: Optional[str] = Field(None, description="Source train station")
    destination_station: str = Field(..., description="Destination train station")

# -----------------------------
# Utility: Haversine distance
# -----------------------------
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # km
    return c * r

# -----------------------------
# Find nearest stations
# -----------------------------
def get_nearest_stations(lat, lon, limit=5):
    stations = list(stations_collection.find({}, {"_id": 0, "name": 1, "lat": 1, "lon": 1}))
    stations_with_distance = []
    for s in stations:
        distance = haversine(lon, lat, s["lon"], s["lat"])
        stations_with_distance.append({**s, "distance_km": distance})
    stations_with_distance.sort(key=lambda x: x["distance_km"])
    return stations_with_distance[:limit]

# -----------------------------
# Save user details & return predicted crowd + nearest stations
# -----------------------------
@router.post("/details")
async def save_user_details(user: UserDetails):
    try:
        # Get coordinates from pincode
        lat, lon = get_coords_from_pincode(user.pincode)

        # Suggest nearest stations if source not provided
        nearest_stations = []
        if not user.source_station:
            nearest_stations = get_nearest_stations(lat, lon)

        # Convert user data to dict
        user_dict = user.dict()

        # -----------------------------
        # Convert dates to strings for MongoDB
        # -----------------------------
        if user_dict.get("from_date"):
            user_dict["from_date"] = user_dict["from_date"].isoformat()
        if user_dict.get("to_date"):
            user_dict["to_date"] = user_dict["to_date"].isoformat()

        # Set closest station as source if not provided
        if not user.source_station and nearest_stations:
            user_dict["source_station"] = nearest_stations[0]["name"]

        # Insert into MongoDB
        users_collection.insert_one(user_dict)

        # -----------------------------
        # Predict crowd if source_station is available
        # -----------------------------
        predicted_crowd = None
        if user_dict.get("source_station"):
            predictor = CrowdPredictor(users_collection)
            predicted_crowd = predictor.predict_crowd(
                journey_time=user.journey_time,
                source=user_dict["source_station"],
                destination=user.destination_station,
                pincode=user.pincode
            )

        return {
            "message": "User details saved successfully!",
            "predicted_crowd": predicted_crowd,
            "nearest_stations": nearest_stations
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

# -----------------------------
# Route to fetch all users (for testing/debug)
# -----------------------------
@router.get("/all")
async def get_all_users():
    try:
        users = list(users_collection.find({}, {"_id": 0}))  # Hide MongoDB _id
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")