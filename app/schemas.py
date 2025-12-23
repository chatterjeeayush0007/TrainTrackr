from pydantic import BaseModel
from typing import List

class TrainSummary(BaseModel):
    train_no: int
    train_name: str

class TrainDetail(BaseModel):
    train_no: int
    train_name: str
    stops: List[dict]

class StationList(BaseModel):
    count: int
    stations: List[str]

class CrowdResponse(BaseModel):
    station: str
    current_hour: int
    train_count: int
    crowd_level: str

class DelayResponse(BaseModel):
    train_no: int
    predicted_delay_minutes: int
    status: str
    expected_time: str
