from enum import Enum
from .base import Base
from sqlalchemy import Column, Integer, String, Float, Enum as Enum_SQLALCHEMY


class FuelChoices(Enum):
    GASOLINE = 'Gasoline'
    DIESEL = 'Diesel'
    GAS = 'Gas'


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    model_name = Column(String(50), nullable=False)
    engine = Column(Float, nullable=False)
    type_of_fuel = Column(Enum_SQLALCHEMY(FuelChoices, name="fuelchoices_type", create_type=True), nullable=False)

    def __init__(self, model, engine, tof):
        self.model_name = model
        self.engine = engine
        self.type_of_fuel = tof

    def __str__(self):
        return f"Car {self.model_name}"

