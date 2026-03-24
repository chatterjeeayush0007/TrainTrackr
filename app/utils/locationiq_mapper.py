# app/utils/locationiq_mapper.py
import requests

# -----------------------------
# Your LocationIQ API Key
# -----------------------------
API_KEY = "pk.26997d1c31b2802036401ef9b6c9b86c"
BASE_URL = "https://us1.locationiq.com/v1/search.php"

# -----------------------------
# Function: Get coordinates from pincode
# -----------------------------
def get_coords_from_pincode(pincode: str):
    """
    Returns (latitude, longitude) tuple for a given Indian pincode.
    Raises Exception if not found.
    """
    try:
        params = {
            "key": API_KEY,
            "q": pincode,
            "format": "json",
            "countrycodes": "IN",
            "limit": 1
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError(f"No coordinates found for pincode {pincode}")
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    except Exception as e:
        raise Exception(f"LocationIQ Error: {str(e)}")