from pydantic import BaseModel
from typing import List, Optional

class Stop(BaseModel):
    station: str
    arrival_time: Optional[str] = None
    departure_time: Optional[str] = None

class Train(BaseModel):
    train_no: int
    train_name: str
    stops: List[Stop]

class Station(BaseModel):
    name: str
