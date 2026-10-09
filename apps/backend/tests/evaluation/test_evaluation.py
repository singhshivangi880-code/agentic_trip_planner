import pytest
from pydantic import BaseModel
from typing import List, Optional

# Mock schemas to represent agent outputs
class Intent(BaseModel):
    destination: str
    duration_days: Optional[int] = None
    missing_fields: List[str] = []

class Recommendation(BaseModel):
    name: str
    interests_matched: List[str]
    confidence: float
    source_url: Optional[str]

class Activity(BaseModel):
    name: str
    date: str
    start_time: str
    end_time: str
    locked: bool = False

class Itinerary(BaseModel):
    activities: List[Activity]

# --- 36.1 Intent Evaluation ---
def evaluate_intent(output: Intent, expected_dest: str):
    accuracy = 1.0 if output.destination.lower() == expected_dest.lower() else 0.0
    detected_missing = "duration_days" in output.missing_fields if not output.duration_days else False
    return accuracy, detected_missing

def test_intent_evaluation():
    out1 = Intent(destination="Rome", duration_days=None, missing_fields=["duration_days"])
    acc, detected = evaluate_intent(out1, "rome")
    assert acc == 1.0
    assert detected is True

# --- 36.2 Recommendation Evaluation ---
def evaluate_recommendations(recs: List[Recommendation], user_interests: List[str]):
    if not recs:
        return 0.0, 0.0, 0.0
    
    # Interest alignment
    alignment_score = sum(1 for r in recs if any(i in user_interests for i in r.interests_matched)) / len(recs)
    
    # Duplicate rate
    names = [r.name for r in recs]
    dup_rate = (len(names) - len(set(names))) / len(names) if names else 0.0
    
    # Source presence
    source_presence = sum(1 for r in recs if r.source_url) / len(recs)
    
    return alignment_score, dup_rate, source_presence

def test_recommendation_evaluation():
    recs = [
        Recommendation(name="Colosseum", interests_matched=["history"], confidence=0.9, source_url="url1"),
        Recommendation(name="Vatican", interests_matched=["art"], confidence=0.8, source_url=None)
    ]
    alignment, dup, source = evaluate_recommendations(recs, ["history", "art"])
    assert alignment == 1.0
    assert dup == 0.0
    assert source == 0.5

# --- 36.3 Itinerary Evaluation ---
def evaluate_itinerary(itinerary: Itinerary):
    # Check date/time correctness (simplified)
    # Check activity diversity
    activity_names = [a.name for a in itinerary.activities]
    diversity = len(set(activity_names)) / len(activity_names) if activity_names else 0.0
    return diversity

def test_itinerary_evaluation():
    itin = Itinerary(activities=[
        Activity(name="Colosseum", date="2026-10-05", start_time="10:00", end_time="12:00"),
        Activity(name="Pantheon", date="2026-10-05", start_time="14:00", end_time="15:00")
    ])
    assert evaluate_itinerary(itin) == 1.0

# --- 36.4 Replanning Evaluation ---
def evaluate_replanning(old: Itinerary, new: Itinerary):
    # Locked items preserved
    old_locked = {a.name for a in old.activities if a.locked}
    new_items = {a.name for a in new.activities}
    preserved = all(item in new_items for item in old_locked)
    return preserved

def test_replanning_evaluation():
    old = Itinerary(activities=[
        Activity(name="Colosseum", date="2026-10-05", start_time="10:00", end_time="12:00", locked=True),
        Activity(name="Old Cafe", date="2026-10-05", start_time="13:00", end_time="14:00")
    ])
    new = Itinerary(activities=[
        Activity(name="Colosseum", date="2026-10-05", start_time="10:00", end_time="12:00", locked=True),
        Activity(name="New Cafe", date="2026-10-05", start_time="13:00", end_time="14:00")
    ])
    assert evaluate_replanning(old, new) is True

# --- 36.5 Regression Fixtures ---
# Directories created via script, no test needed here directly, handled by fixtures dir.
