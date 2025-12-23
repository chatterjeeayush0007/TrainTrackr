from datetime import datetime

# Base delay (minutes) for known trains
TRAIN_BASE_DELAYS = {
    101: 2,
    102: 5,
    103: 10,
    104: 0,
}


def predict_delay(train_no: int) -> int:
    """
    Predict delay for a local train using simple heuristics.

    Logic:
    - Base delay per train (if known)
    - Peak hour adjustment
    """
    if not isinstance(train_no, int):
        raise ValueError("train_no must be an integer")

    base_delay = TRAIN_BASE_DELAYS.get(train_no, 3)  # default if unknown

    hour = datetime.now().hour
    is_peak_hour = (7 <= hour <= 10) or (17 <= hour <= 20)

    peak_delay = 5 if is_peak_hour else 0

    return base_delay + peak_delay
