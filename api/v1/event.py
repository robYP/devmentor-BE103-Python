from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import repository.event
from infrastructure.mysql import get_db
from schema.database.event import EventCreate

router = APIRouter(
    tags=["events"],
    prefix="/events"
)

@router.get("/")
def list_event(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = repository.event.get_events(db, skip=skip, limit=limit)
    return events

@router.post("/")
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    event = repository.event.create_event(event, db)
    return event