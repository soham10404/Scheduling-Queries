from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker     
import pymysql

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Gudiya@localhost:3306/TEST_DB"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()
