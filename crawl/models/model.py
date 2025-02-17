from sqlalchemy.orm import DeclarativeBase, relationship, Mapped
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from typing import List

class Base(DeclarativeBase):
    pass


class AirlineModel(Base):
    __tablename__ = "airline"
    airline_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    aircrafts: Mapped[List["AirCraftModel"]] = relationship(back_populates="airline")

    
class AirCraftModel(Base):
    __tablename__ = "aircraft"
    aircraft_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    airline_id = Column(Integer, ForeignKey("airline.airline_id"))
    type = Column(String, nullable=False)
    airline: Mapped["AirlineModel"] = relationship(back_populates="aircrafts")
    flights: Mapped[List["FlightModel"]] = relationship(back_populates="aircraft")


class FlightModel(Base):
    __tablename__ = "flight"
    flight_id = Column(Integer, primary_key=True)
    flight_number = Column(String, nullable=False)
    aircraft_id = Column(Integer, ForeignKey("aircraft.aircraft_id"))
    airline_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    from_airport = Column(String, nullable=False)
    to_airport = Column(String, nullable=False)
    scheduled_time_of_departure = Column(String, nullable=False)
    scheduled_time_of_arrival = Column(String, nullable=False)
    status = Column(String, nullable=False)
    actual_time_of_departure = Column(String, nullable=False)
    actual_time_of_arrival = Column(String, nullable=False)
    aircraft: Mapped["AirCraftModel"] = relationship(back_populates="flights")