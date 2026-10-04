from datetime import date, datetime
from typing import Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, model_validator, ConfigDict
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.trip_repository import TripRepository

router = APIRouter(prefix="/trips", tags=["trips"])

class TripPreferences(BaseModel):
    budget: Optional[Literal["budget", "moderate", "luxury"]] = None
    pace: Optional[Literal["relaxed", "balanced", "packed"]] = None
    interests: Optional[list[str]] = None
    group_composition: Optional[str] = None

class TripCreateRequest(BaseModel):
    origin: Optional[str] = None
    destination: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration_days: int = Field(ge=1)
    nationality: Optional[str] = None
    preferences: Optional[TripPreferences] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValueError("start_date cannot be after end_date")
        return self

class TripPatchRequest(BaseModel):
    status: str

class TripResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    profile_id: Optional[str] = None
    title: str
    origin: Optional[str] = None
    destination: str
    start_date: Optional[str] = None  # model stores as string currently
    end_date: Optional[str] = None
    duration_days: int
    status: str
    workflow_status: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

def get_trip_repo(db: Session = Depends(get_db)) -> TripRepository:
    return TripRepository(db)

@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(
    request: TripCreateRequest,
    repo: TripRepository = Depends(get_trip_repo)
):
    # ponytail: mapped explicitly inline. Repositories handle the persistence.
    trip = repo.create_trip(
        destination=request.destination,
        duration_days=request.duration_days,
        origin=request.origin,
        title=f"Trip to {request.destination}",
        preferences=request.preferences.model_dump() if request.preferences else {},
        start_date=request.start_date,
        end_date=request.end_date
    )
    return trip

@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: str,
    repo: TripRepository = Depends(get_trip_repo)
):
    trip = repo.get_trip_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.patch("/{trip_id}", response_model=TripResponse)
def patch_trip(
    trip_id: str,
    request: TripPatchRequest,
    repo: TripRepository = Depends(get_trip_repo)
):
    trip = repo.update_trip_status(trip_id, request.status)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip
