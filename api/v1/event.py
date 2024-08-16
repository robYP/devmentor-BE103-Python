from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

import repository.event, repository.record
from infrastructure.mysql import get_db
from schema.database.event import EventCreate
from services.auth import get_current_user

router = APIRouter(
    tags=["events"],
    prefix="/events"
)

@router.get("/")
def list_event(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = repository.event.get_events(db, skip=skip, limit=limit)
    return events

@router.post("/")
def create_event(user: Annotated[dict, Depends(get_current_user)], event: EventCreate, db: Session = Depends(get_db)):
    event = repository.event.create_event(user=user, event=event, db=db)
    repository.record.create_record(user_id = user.id,
                                    event_id = event.id,
                                    action = "Create Event",
                                    db=db)
    return event


@router.delete("/{event_id}")
def delete_event_by_id(user: Annotated[dict, Depends(get_current_user)], event_id:int, db:Session = Depends(get_db)):
    event = repository.event.delete_event_by_id(db=db, event_id=event_id)
    if event == None: 
        raise HTTPException(status_code=404, detail="Event Not Found")
    repository.record.create_record(user_id = user.id,
                                    event_id = event_id,
                                    action = "Delete Event",
                                    db=db)
    return event


@router.put("/{event_id}")
def update_event_by_id(user: Annotated[dict, Depends(get_current_user)],event_id: int, event: EventCreate, db: Session = Depends(get_db)):
    event = repository.event.update_event_by_id(user=user, event_id=event_id, event=event, db=db)
    if event == None:
        raise HTTPException(status_code=404, detail="Event Not Found")
    repository.record.create_record(user_id = user.id,
                                    event_id = event.id,
                                    action = "Update Event",
                                    db=db)
    return event