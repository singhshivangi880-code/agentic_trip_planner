import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    profile_id = Column(String, ForeignKey("traveller_profiles.id"), nullable=True)
    title = Column(String, nullable=False)
    origin = Column(String, nullable=True)
    destination = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    duration_days = Column(Integer, default=1)
    status = Column(String, default="draft")
    preferences = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    days = relationship("TripDay", back_populates="trip", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="trip", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="trip", cascade="all, delete-orphan")
    versions = relationship("TripVersion", back_populates="trip", cascade="all, delete-orphan")


class TripVersion(Base):
    __tablename__ = "trip_versions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id = Column(String, ForeignKey("trips.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    state_snapshot = Column(JSON, nullable=False)
    change_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    trip = relationship("Trip", back_populates="versions")
