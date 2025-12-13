from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from app.utils.delay_predict import predict_delay

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)

@router.get("/delay/{train_no}")
def delay_prediction(train_no: int):
    """
    Predict delay for a train using local train schedule and heuristics
    """
    try:
        # Compute delay (minutes)
        delay_minutes = predict_delay(train_no)

        # Example logic: small delays are "On Time", bigger delays are "Delayed"
        status = "On Time" if delay_minutes <= 5 else "Delayed"

        # Estimate expected arrival (current time + delay)
        now = datetime.now()
        expected_arrival = now + timedelta(minutes=delay_minutes)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "train_no": train_no,
        "predicted_delay_minutes": delay_minutes,
        "status": status,
        "expected_time": expected_arrival.strftime("%H:%M:%S")
    }
