import pytest
from agents.validation.validators.engine import validate_itinerary
from agents.itinerary.schema import Itinerary, TripDay, ItineraryItem

def test_validation_engine():
    # Valid
    valid_itin = Itinerary(days=[
        TripDay(day_index=1, date="2026-10-01", theme_or_area="Tokyo", items=[
            ItineraryItem(title="A", description="A", start_time="09:00", end_time="10:00", location="Loc", item_type="Activity"),
            ItineraryItem(title="B", description="B", start_time="10:30", end_time="12:00", location="Loc", item_type="Activity")
        ])
    ])
    res = validate_itinerary(valid_itin, "2026-10-01", "2026-10-03")
    assert res.is_valid
    assert len(res.errors) == 0

    # Overlap and inverted times
    invalid_itin = Itinerary(days=[
        TripDay(day_index=1, date="2026-10-01", theme_or_area="Tokyo", items=[
            ItineraryItem(title="A", description="A", start_time="10:00", end_time="09:00", location="Loc", item_type="Activity"),
            ItineraryItem(title="B", description="B", start_time="08:00", end_time="12:00", location="Loc", item_type="Activity")
        ])
    ])
    res = validate_itinerary(invalid_itin, "2026-10-01", "2026-10-03")
    assert not res.is_valid
    assert len(res.errors) >= 2
    assert "start time >= end time" in res.errors[0]
    assert "overlaps" in res.errors[1]

    # Out of bounds date
    bounds_itin = Itinerary(days=[
        TripDay(day_index=1, date="2026-10-05", theme_or_area="Tokyo", items=[])
    ])
    res = validate_itinerary(bounds_itin, "2026-10-01", "2026-10-03")
    assert not res.is_valid
    assert "outside trip bounds" in res.errors[0]

    # Duplicates
    dup_itin = Itinerary(days=[
        TripDay(day_index=1, date="2026-10-01", theme_or_area="Tokyo", items=[
            ItineraryItem(title="Temple", description="A", start_time="09:00", end_time="10:00", location="Loc", item_type="Activity"),
            ItineraryItem(title="Temple", description="B", start_time="10:30", end_time="12:00", location="Loc", item_type="Activity")
        ])
    ])
    res = validate_itinerary(dup_itin, "2026-10-01", "2026-10-03")
    assert res.is_valid # warnings don't invalidate
    assert len(res.warnings) == 1
    assert "duplicate" in res.warnings[0]
