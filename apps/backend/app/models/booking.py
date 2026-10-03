import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id = Column(String, ForeignKey("trips.id"), nullable=False)
    type = Column(String, nullable=False) # flight, train, bus, hotel, tour, ticket, reservation
    title = Column(String, nullable=False)
    provider = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    reference_number = Column(String, nullable=True)
    cost = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    locked = Column(Boolean, default=True) # Fixed planning anchor

    trip = relationship("Trip", back_populates="bookings")
