import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()


database = create_engine(os.getenv("DATABASE_URL"))

Session = sessionmaker(database)
session = Session()

Base = declarative_base()

def create_db():
    Base.metadata.create_all(database)

def drop_db():
    Base.metadata.drop_all(database)
