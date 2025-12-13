from datetime import datetime

# Example: local train delay heuristics
# You can expand this with real local stats
TRAIN_BASE_DELAYS = {
    101: 2,
    102: 5,
    103: 10,
    104: 0,
}

def predict_delay(train_no: int) -> int:
    """
    Predict delay for a local train using simple heuristics
    """
    base_delay = TRAIN_BASE_DELAYS.get(train_no, 3)  # default 3 min if unknown

    # Additional logic: peak hours add more delay
    hour = datetime.now().hour
    if 7 <= hour <= 10 or 17 <= hour <= 20:
        peak_delay = 5
    else:
        peak_delay = 0

    return base_delay + peak_delay
