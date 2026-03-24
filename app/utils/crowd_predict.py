# app/utils/crowd_predict.py

import json
from pathlib import Path

class CrowdPredictor:
    """
    Predicts crowd level for trains based on:
    - App usage fraction (5-10% of pincode population)
    - Growth rate from survey (mocked in JSON)
    - Optional MongoDB data of actual check-ins
    """

    def __init__(self, users_collection, population_file=None):
        """
        users_collection: MongoDB collection of user check-ins or app usage
        population_file: JSON file with pincode population and growth rate
        """
        self.users_collection = users_collection
        self.population_file = population_file or Path(__file__).resolve().parent.parent / "data" / "pincode_population.json"

        # Load pincode population data
        try:
            with open(self.population_file, "r", encoding="utf-8") as f:
                self.pincode_data = json.load(f)
        except FileNotFoundError:
            self.pincode_data = {}

    def predict_crowd_for_train(self, train_no, pincode=None):
        """
        Estimate crowd for a train:
        - base on app usage (5% of pincode population if given)
        - include growth factor
        - add MongoDB check-ins if available
        - fallback: minimal 10 users if no data
        """

        base_users = 10  # fallback if nothing else available

        if pincode and pincode in self.pincode_data:
            pop_info = self.pincode_data[pincode]
            population = pop_info.get("population", 10000)  # default 10k
            growth_rate = pop_info.get("growth_rate", 0.02)  # default 2% growth

            # assume 5-10% of population uses app
            usage_fraction = 0.05
            estimated_users = int(population * usage_fraction)

            # add growth rate
            estimated_users = int(estimated_users * (1 + growth_rate))
            base_users = estimated_users

        # Optionally add MongoDB data influence
        if self.users_collection:
            try:
                db_count = self.users_collection.count_documents({"train_no": train_no})
                base_users += db_count
            except Exception:
                pass

        return base_users