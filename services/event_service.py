from sqlalchemy.orm import Session
from schema.database.event import EventCreate

from repository.event import EventRepository
from repository.record import RecordRepository


class EventService:
    def __init__(self, db: Session):
        self.event_repository = EventRepository(db=db)
        self.record_repository = RecordRepository(db=db)
        self.db = db
        

    def list_event(self, skip: int = 0, limit: int = 100):
        events = self.event_repository.get_events(skip=skip, limit=limit)
        return events


    def create_event(self, user: dict, event: EventCreate):
        new_event = self.event_repository.create_event(user=user, event=event)
        self.record_repository.create_record(user_id = user.id,
                                       event_id = new_event.id,
                                       action = "Create Event")
        return new_event


    def delete_event_by_id(self, user: dict, event_id: int):
        event = self.event_repository.delete_event_by_id(event_id=event_id)
        if event:
            self.record_repository.create_record(user_id = user.id,
                                           event_id = event.id,
                                           action = "Delete Event")
        return event


    def update_event_by_id(self, user: dict, event_id: int, event: EventCreate):
        updated_event = self.event_repository.update_event_by_id(event_id=event_id, event=event)
        if updated_event:
            self.record_repository.create_record(user_id = user.id,
                                       event_id = updated_event.id,
                                       action = "Update Event")
        return updated_event