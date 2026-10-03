from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.trip import Trip, TripVersion
from app.models.itinerary import TripDay, ItineraryItem
from app.models.booking import Booking


class TripRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_trip(self, destination: str, duration_days: int, origin: Optional[str] = None, title: Optional[str] = None, preferences: Optional[dict] = None) -> Trip:
        trip = Trip(
            title=title or f"Trip to {destination}",
            destination=destination,
            duration_days=duration_days,
            origin=origin,
            preferences=preferences or {},
        )
        self.db.add(trip)
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def get_trip_by_id(self, trip_id: str) -> Optional[Trip]:
        return self.db.query(Trip).filter(Trip.id == trip_id).first()

    def list_trips(self, user_id: Optional[str] = None) -> List[Trip]:
        query = self.db.query(Trip)
        if user_id:
            query = query.filter(Trip.user_id == user_id)
        return query.all()

    def update_trip_status(self, trip_id: str, status: str) -> Optional[Trip]:
        trip = self.get_trip_by_id(trip_id)
        if trip:
            trip.status = status
            self.db.commit()
            self.db.refresh(trip)
        return trip

    def delete_trip(self, trip_id: str) -> bool:
        trip = self.get_trip_by_id(trip_id)
        if trip:
            self.db.delete(trip)
            self.db.commit()
            return True
        return False

    def add_booking(self, trip_id: str, type: str, title: str, **kwargs) -> Booking:
        booking = Booking(trip_id=trip_id, type=type, title=title, **kwargs)
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking
