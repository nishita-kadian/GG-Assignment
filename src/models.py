from pydantic import BaseModel
from uuid import uuid4, UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Float, Double, DateTime, Date, Time
import uuid
from datetime import datetime, date, time

Base = declarative_base()

class EventModel(BaseModel):
    eventId: UUID
    eventName: str
    cityName: str
    date: date
    time: time
    latitude: float 
    longitude: float
    # weather: str
    # distance: float


class Event(Base):
    __tablename__ = "event"
    eventId = Column(String, primary_key=True)
    eventName = Column(String)
    cityName = Column(String)
    date = Column(Date)
    time = Column(Time) 
    latitude = Column(Double)
    longitude = Column(Double)
    # weather = Column(String)
    # distance_km = Column(Double)

class EventAdapter:
    def __init__(self, eventModel):
        self.eventModel = eventModel
    
    def to_event(self):
        return Event(
            eventId=str(self.eventModel.eventId),
            eventName=self.eventModel.eventName,
            cityName=self.eventModel.cityName,
            date=self.eventModel.date,
            time=self.eventModel.time,
            latitude=self.eventModel.latitude,
            longitude=self.eventModel.longitude,
            # weather=self.eventModel.weather,
            # distance_km=self.eventModel.distance
        )

