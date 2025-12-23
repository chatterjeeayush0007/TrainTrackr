from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from app.utils.train_assistant_logic import find_best_train_backend

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)

@router.get("/")
def get_recommendation(
    start_station: str = Query(..., description="Starting station"),
    dest_station: str = Query(..., description="Destination station"),
    arrival_time: str = Query(..., description="Desired arrival time HH:MM")
):
    try:
        result, status = find_best_train_backend(start_station, dest_station, arrival_time)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail="No trains found for this route")

    return {
        "status": status,
        "train_no": result["train_no"],
        "train_name": result["train_name"],
        "expected_arrival": result["expected_arrival"].strftime("%H:%M"),
        "delay": result["delay"],
        "crowd": result["crowd"],
        "time_diff": result["time_diff"]
    }
