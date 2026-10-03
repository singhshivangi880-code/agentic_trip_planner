import uuid
from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.db import Base


class TripDay(Base):
    __tablename__ = "trip_days"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id = Column(String, ForeignKey("trips.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(String, nullable=True)
    theme = Column(String, nullable=True)
    city = Column(String, nullable=True)

    trip = relationship("Trip", back_populates="days")
    items = relationship("ItineraryItem", back_populates="day", cascade="all, delete-orphan")


class ItineraryItem(Base):
    __tablename__ = "itinerary_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_day_id = Column(String, ForeignKey("trip_days.id"), nullable=False)
    type = Column(String, nullable=False) # attraction, experience, meal, transport, booking, note
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_time = Column(String, nullable=True)
    end_time = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    locked = Column(Boolean, default=False)
    visited = Column(Boolean, default=False)
    confidence = Column(String, default="HIGH")
    verify_directly_note = Column(String, nullable=True)
    extra_metadata = Column(JSON, default=dict)

    day = relationship("TripDay", back_populates="items")
