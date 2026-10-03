import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.db import Base
from app.repositories.trip_repository import TripRepository
from app.models.user import User
from app.models.profile import TravellerProfile


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_user_creation(db_session):
    user = User(email="test@example.com", name="Test User")
    db_session.add(user)
    db_session.commit()

    fetched = db_session.query(User).filter_by(email="test@example.com").first()
    assert fetched is not None
    assert fetched.name == "Test User"


def test_trip_repository_crud(db_session):
    repo = TripRepository(db_session)
    
    # Create
    trip = repo.create_trip(destination="Japan", duration_days=10, origin="Pune", preferences={"pace": "relaxed"})
    assert trip.id is not None
    assert trip.destination == "Japan"
    
    # Read
    fetched = repo.get_trip_by_id(trip.id)
    assert fetched is not None
    assert fetched.title == "Trip to Japan"
    
    # Add Booking
    booking = repo.add_booking(trip_id=trip.id, type="flight", title="Flight to Tokyo", provider="Japan Airlines")
    assert booking.id is not None
    assert booking.locked is True
    
    # Delete
    deleted = repo.delete_trip(trip.id)
    assert deleted is True
    assert repo.get_trip_by_id(trip.id) is None
