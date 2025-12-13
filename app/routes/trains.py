from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter(
    prefix="/trains",
    tags=["Trains"]
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "trains.json"


def load_trains():
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="trains.json not found")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/")
def get_all_trains():
    """
    Returns basic info of all trains
    """
    data = load_trains()

    trains = [
        {
            "train_no": train.get("train_no"),
            "train_name": train.get("train_name")
        }
        for train in data
    ]

    return {
        "count": len(trains),
        "trains": trains
    }


@router.get("/{train_no}")
def get_train_by_number(train_no: int):
    """
    Returns full details of a specific train
    """
    data = load_trains()

    for train in data:
        if train.get("train_no") == train_no:
            return train

    raise HTTPException(status_code=404, detail="Train not found")


@router.get("/{train_no}/route")
def get_train_route(train_no: int):
    """
    Returns route (stops) of a train
    """
    data = load_trains()

    for train in data:
        if train.get("train_no") == train_no:
            return {
                "train_no": train_no,
                "train_name": train.get("train_name"),
                "stops": train.get("stops", [])
            }

    raise HTTPException(status_code=404, detail="Train not found")
