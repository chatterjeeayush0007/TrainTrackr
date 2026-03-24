# Sample GPS Mapper logic

# Mock database of stations with lat/lon
STATIONS_DB = [
    {"name": "Station A", "lat": 19.0760, "lon": 72.8777},
    {"name": "Station B", "lat": 19.2183, "lon": 72.9781},
    {"name": "Station C", "lat": 19.0510, "lon": 73.0120},
]

# Mock mapping of pincode -> coordinates
PINCODE_GPS = {
    "400001": (19.075983, 72.877655),
    "400002": (19.085000, 72.900000),
    "400003": (19.100000, 72.920000),
}

from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    # Calculate distance in km
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def get_nearest_stations(pincode: str, top_n: int = 3):
    if pincode not in PINCODE_GPS:
        raise ValueError("Pincode not mapped to GPS coordinates")
    user_lat, user_lon = PINCODE_GPS[pincode]

    station_distances = []
    for s in STATIONS_DB:
        dist = haversine(user_lat, user_lon, s["lat"], s["lon"])
        station_distances.append({"name": s["name"], "distance": round(dist, 2)})

    # Sort by distance
    station_distances.sort(key=lambda x: x["distance"])
    return station_distances[:top_n]