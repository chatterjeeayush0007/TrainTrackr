# Utility functions for time calculations
from datetime import datetime, timedelta

def add_minutes(time: datetime, minutes: int) -> datetime:
    return time + timedelta(minutes=minutes)
