import os
from datetime import date, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models  # noqa: F401 - register all models on Base.metadata
from app.core.db import Base
from app.repositories.trip_repository import TripRepository
from app.models.user import User
from app.models.profile import TravellerProfile
from app.models.trip import Trip, TripVersion
from app.models.itinerary import TripDay, ItineraryItem
from app.models.recommendation import Recommendation
from app.models.booking import Booking

# Always test against in-memory SQLite. Set TEST_DATABASE_URL (e.g. the docker-compose Postgres)
# to also run the same suite against PostgreSQL - this is Connectivity Check C5.
DB_URLS = ["sqlite:///:memory:"]
if os.getenv("TEST_DATABASE_URL"):
    DB_URLS.append(os.environ["TEST_DATABASE_URL"])


@pytest.fixture(params=DB_URLS, ids=lambda u: u.split(":")[0])
def db_session(request):
    engine = create_engine(request.param)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def trip(db_session):
    return TripRepository(db_session).create_trip(destination="Japan", duration_days=10, origin="Pune")


def crud(db_session, obj, update_field, update_value):
    """Create, read, update, delete a single model instance."""
    model = type(obj)
    db_session.add(obj)
    db_session.commit()
    assert obj.id is not None

    fetched = db_session.get(model, obj.id)
    assert fetched is not None

    setattr(fetched, update_field, update_value)
    db_session.commit()
    db_session.expire_all()
    assert getattr(db_session.get(model, obj.id), update_field) == update_value

    db_session.delete(fetched)
    db_session.commit()
    assert db_session.get(model, obj.id) is None


def test_user_creation(db_session):
    user = User(email="test@example.com", name="Test User")
    db_session.add(user)
    db_session.commit()

    fetched = db_session.query(User).filter_by(email="test@example.com").first()
    assert fetched is not None
    assert fetched.name == "Test User"


def test_user_crud(db_session):
    crud(db_session, User(email="crud@example.com", name="A"), "name", "B")


def test_profile_crud(db_session):
    profile = TravellerProfile(name="Akshay", home_city="Pune", interests=["food", "temples"])
    crud(db_session, profile, "pace", "relaxed")


def test_trip_version_crud(db_session, trip):
    version = TripVersion(trip_id=trip.id, version_number=1, state_snapshot={"days": []}, change_reason="initial")
    crud(db_session, version, "change_reason", "replanned")


def test_trip_day_and_item_crud(db_session, trip):
    day = TripDay(trip_id=trip.id, day_number=1, date=date(2027, 2, 8), city="Tokyo")
    db_session.add(day)
    db_session.commit()
    item = ItineraryItem(trip_day_id=day.id, type="attraction", name="Senso-ji", start_time="09:00")
    crud(db_session, item, "locked", True)
    crud(db_session, day, "theme", "Old Tokyo")


def test_recommendation_crud(db_session, trip):
    rec = Recommendation(trip_id=trip.id, name="Yanaka", category="neighbourhood", classification="offbeat")
    crud(db_session, rec, "confidence", "MODERATE")


def test_booking_crud(db_session, trip):
    booking = Booking(trip_id=trip.id, type="hotel", title="Hotel Gracery", start_time=datetime(2027, 2, 8, 15, 0))
    crud(db_session, booking, "reference_number", "ABC123")


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
    assert len(repo.list_trips()) == 1

    # Update
    updated = repo.update_trip_status(trip.id, "planning")
    assert updated.status == "planning"

    # Add Booking
    booking = repo.add_booking(trip_id=trip.id, type="flight", title="Flight to Tokyo", provider="Japan Airlines")
    assert booking.id is not None
    assert booking.locked is True

    # Delete (cascades to bookings)
    deleted = repo.delete_trip(trip.id)
    assert deleted is True
    assert repo.get_trip_by_id(trip.id) is None
    assert db_session.get(Booking, booking.id) is None


def test_create_trip_with_dates_derives_duration(db_session):
    trip = TripRepository(db_session).create_trip(
        destination="Japan", start_date=date(2027, 2, 8), end_date=date(2027, 2, 18)
    )
    assert trip.duration_days == 11
    assert trip.start_date == date(2027, 2, 8)
