import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from app.core.db import Base


class TravellerProfile(Base):
    __tablename__ = "traveller_profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    home_city = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    pace = Column(String, default="balanced")
    budget = Column(String, default="moderate")
    dietary_preferences = Column(JSON, default=list)
    interests = Column(JSON, default=list)
    group_defaults = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
