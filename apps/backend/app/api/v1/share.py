from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from datetime import datetime
from pydantic import BaseModel

from app.core.db import get_db
from app.models.trip import Trip
from app.models.share import TripShare

from app.core.security import rate_limit, User, require_current_user
from app.api.v1.trips import TripRepository, get_trip_repo

router = APIRouter()

class ShareCreate(BaseModel):
    trip_id: str

class ShareResponse(BaseModel):
    token: str
    expires_at: datetime

@router.post("/", response_model=ShareResponse, dependencies=[rate_limit(times=10, seconds=60)])
def create_share(
    req: ShareCreate, 
    db: Session = Depends(get_db),
    repo: TripRepository = Depends(get_trip_repo),
    user: User = Depends(require_current_user)
) -> Any:
    trip = repo.get_trip_by_id(req.trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.user_id and trip.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this trip")
        
    share = db.query(TripShare).filter(TripShare.trip_id == req.trip_id).first()
    if not share:
        share = TripShare(trip_id=req.trip_id)
        db.add(share)
        db.commit()
        db.refresh(share)
        
    return ShareResponse(token=share.token, expires_at=share.expires_at)

@router.get("/{token}", dependencies=[rate_limit(times=60, seconds=60)])
def get_shared_trip(token: str, db: Session = Depends(get_db)) -> Any:
    share = db.query(TripShare).filter(TripShare.token == token).first()
    if not share:
        raise HTTPException(status_code=404, detail="Share link not found")
        
    if share.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Share link expired")
        
    trip = db.query(Trip).filter(Trip.id == share.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    # Read-only subset that doesn't leak user/profile IDs
    return {
        "title": trip.title,
        "destination": trip.destination,
        "start_date": trip.start_date,
        "end_date": trip.end_date,
        "days": [
            {
                "date": day.date,
                "theme_or_area": day.theme_or_area,
                "items": [
                    {
                        "title": item.title,
                        "item_type": item.item_type,
                        "start_time": item.start_time.strftime("%H:%M") if item.start_time else None,
                        "end_time": item.end_time.strftime("%H:%M") if item.end_time else None,
                        "location": item.location,
                        "description": item.description,
                        "is_locked": item.is_locked,
                    }
                    for item in day.items
                ]
            }
            for day in trip.days
        ]
    }
