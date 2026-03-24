# app/routes/railradar.py
from fastapi import APIRouter, Query, HTTPException
import requests
import os

router = APIRouter(
    prefix="/railradar",
    tags=["RailRadar"]
)

# Load API key from env or fallback
RAILRADAR_API_KEY = os.getenv("RAILRADAR_API_KEY", "rr_b8phb55xxb21gw579lnr9y7bwdn1883w")

# ✅ Updated Base URL to match the curl example
BASE_URL = "https://api.railradar.org/api/v1"

# -----------------------------
# 🚆 Get train details by number
# -----------------------------
@router.get("/train/{train_no}")
def get_train(train_no: str):
    url = f"{BASE_URL}/trains/{train_no}"
    headers = {"X-API-Key": RAILRADAR_API_KEY}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
        if not data.get("success", False):
            raise HTTPException(status_code=400, detail=data.get("message", "API returned error"))
        return {"success": True, "data": data.get("data", {})}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"RailRadar API request failed: {str(e)}")


# -----------------------------
# 🔍 Search stations
# -----------------------------
@router.get("/stations/search")
def search_stations(query: str = Query(..., min_length=1)):
    url = f"{BASE_URL}/stations/search"
    headers = {"X-API-Key": RAILRADAR_API_KEY}
    params = {"query": query}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        if not data.get("success", False):
            raise HTTPException(status_code=400, detail=data.get("message", "API returned error"))
        return {"success": True, "stations": data.get("data", [])}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"RailRadar API request failed: {str(e)}")