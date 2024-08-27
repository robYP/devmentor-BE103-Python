from sqlalchemy.orm import Session
import repository.event, repository.record
from schema.database.event import EventCreate


class EventService:
    def __init__(self, db: Session):
        self.db = db
        

    def list_event(self, skip: int = 0, limit: int = 100):
        events = repository.event.get_events(db=self.db, skip=skip, limit=limit)
        return events


    def create_event(self, user: dict, event: EventCreate):
        new_event = repository.event.create_event(user=user, event=event, db=self.db)
        repository.record.create_record(user_id=user.id,
                                        event_id=new_event.id,
                                        action="Create Event",
                                        db=self.db)
        return new_event

    def delete_event_by_id(self, user: dict, event_id: int):
        event = repository.event.delete_event_by_id(db=self.db, event_id=event_id)
        if event:
            repository.record.create_record(user_id=user.id,
                                            event_id=event_id,
                                            action="Delete Event",
                                            db=self.db)
        return event

    def update_event_by_id(self, user: dict, event_id: int, event: EventCreate):
        updated_event = repository.event.update_event_by_id(user=user, event_id=event_id, event=event, db=self.db)
        if updated_event:
            repository.record.create_record(user_id=user.id,
                                            event_id=updated_event.id,
                                            action="Update Event",
                                            db=self.db)
        return updated_event