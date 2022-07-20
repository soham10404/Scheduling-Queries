import enum
from database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Enum

class Query_Status(enum.Enum):
    Awaiting = 'Awaiting'
    Declined = 'Declined'
    Approved = 'Approved'

class Write_pref(enum.Enum):
    Append = 'Append to table'
    Overwrite = 'Overwrite table'

class Query(Base):
    __tablename__ = "Query"
    id = Column(Integer, primary_key = True, index = True)
    # user_id = Column(String(100));
    query = Column(String(11000))
    repeats = Column(String(250))
    repeats_instance = Column(String(100))
    title = Column(String(250))
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    status = Column(Enum(Query_Status))
    table_id = Column(String(250))
    dataset = Column(String(250))
    partitioning_field = Column(String(250))
    write_preference = Column(Enum(Write_pref))
    location = Column(String(250))
    notify_via_mail = Column(Boolean, default = False)
    # is_scheduled = Column(Boolean, default = False)

class Jira(Base):
    __tablename__ =  "Jira"
    key = Column(String(100))
    id = Column(Integer, index = True, primary_key = True)
    status = Column(Enum(Query_Status))

class Bigquery(Base):
    __tablename__ = "Bigquery"
    key = Column(String(250))
    config_name = Column(String(250))
    