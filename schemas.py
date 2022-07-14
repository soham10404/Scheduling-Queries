from pydantic import BaseModel
from models import Write_pref, Query_Status
from datetime import datetime

class QuerySchema(BaseModel):
    # user_id: str
    query: str
    repeats:  str
    repeats_instance: str
    title: str
    startTime: datetime
    endTime: datetime
    status: Query_Status
    table_id: str
    dataset: str
    partitioning_field: str
    write_preference: Write_pref
    location: str
    notify_via_mail: bool

    class Config: 
        orm_mode: True