import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id = Column(String, ForeignKey("trips.id"), nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    classification = Column(String, default="tourist") # tourist vs offbeat
    reason = Column(String, nullable=True)
    confidence = Column(String, default="HIGH")
    extra_metadata = Column(JSON, default=dict)
    last_checked_at = Column(DateTime, default=datetime.utcnow)

    trip = relationship("Trip", back_populates="recommendations")
