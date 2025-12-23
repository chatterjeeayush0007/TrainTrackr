from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter(
    prefix="/stations",
    tags=["Stations"]
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "trains.json"


def load_trains():
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="trains.json not found")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise HTTPException(status_code=500, detail="Invalid trains data format")

    return data


@router.get("/")
def get_all_stations():
    """Returns unique list of stations"""
    data = load_trains()

    stations = set()
    for train in data:
        for stop in train.get("stops", []):
            station = stop.get("station")
            if station:
                stations.add(station)

    return {
        "count": len(stations),
        "stations": sorted(stations)
    }


@router.get("/search")
def search_station(q: str):
    """Search station by name"""
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")

    data = load_trains()
    results = set()

    for train in data:
        for stop in train.get("stops", []):
            station = stop.get("station", "")
            if q.lower() in station.lower():
                results.add(station)

    if not results:
        raise HTTPException(status_code=404, detail="No stations found")

    return {
        "query": q,
        "results": sorted(results)
    }
