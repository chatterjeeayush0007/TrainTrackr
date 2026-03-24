from datetime import datetime, timedelta
from pymongo.collection import Collection
from typing import List, Dict
import math

# -----------------------------
# Crowd Prediction Logic
# -----------------------------

class CrowdPredictor:
    """
    Predicts the expected number of passengers on a train based on:
    - User inputs
    - Historical/registered app users
    - Population growth factor
    """

    def __init__(self, users_collection: Collection):
        self.users_collection = users_collection
        # Percentage of total population using the app (configurable)
        self.app_user_fraction = 0.05  # 5% default

    def _get_users_by_time(self, journey_time: str, source: str, destination: str) -> List[Dict]:
        """
        Fetch users traveling at the same time between source and destination.
        journey_time: "HH:MM" string
        """
        users = list(self.users_collection.find({
            "source": source,
            "destination": destination,
            "journey_time": journey_time
        }))
        return users

    def _population_factor(self, pincode: str) -> float:
        """
        Dummy population growth logic.
        Normally you would fetch government reports or census projections.
        For simplicity, assume growth factor 1–1.1
        """
        # Here, we simulate a growth factor
        growth_factor = 1.05  # +5% increase
        return growth_factor

    def predict_crowd(self, journey_time: str, source: str, destination: str, pincode: str) -> int:
        """
        Predict number of passengers for a given train segment
        """
        # 1. Count registered app users for this journey
        users = self._get_users_by_time(journey_time, source, destination)
        app_users_count = len(users)

        # 2. Scale by app usage fraction (assume only 5–10% of people use the app)
        estimated_total_users = app_users_count / self.app_user_fraction

        # 3. Apply population growth factor
        factor = self._population_factor(pincode)
        predicted_crowd = int(math.ceil(estimated_total_users * factor))

        return predicted_crowd

    def predict_for_day(self, date: datetime, source: str, destination: str, pincode: str) -> Dict[str, int]:
        """
        Predict crowd for all trains throughout the day between source and destination
        Returns: { 'HH:MM': predicted_count }
        """
        predictions = {}
        # Example: assume trains every 30 min from 6:00 to 22:00
        start_time = datetime.combine(date.date(), datetime.strptime("06:00", "%H:%M").time())
        end_time = datetime.combine(date.date(), datetime.strptime("22:00", "%H:%M").time())
        current_time = start_time

        while current_time <= end_time:
            time_str = current_time.strftime("%H:%M")
            predictions[time_str] = self.predict_crowd(time_str, source, destination, pincode)
            current_time += timedelta(minutes=30)

        return predictions

# -----------------------------
# Example usage (for testing)
# -----------------------------
if __name__ == "__main__":
    from app.db.mongodb import get_db_client

    client = get_db_client()
    db = client["traintrackr"]
    users_collection = db["users"]

    predictor = CrowdPredictor(users_collection)

    pred = predictor.predict_crowd("08:30", "Mumbai CST", "Thane", "400001")
    print(f"Predicted passengers at 08:30: {pred}")

    day_pred = predictor.predict_for_day(datetime.today(), "Mumbai CST", "Thane", "400001")
    print(day_pred)