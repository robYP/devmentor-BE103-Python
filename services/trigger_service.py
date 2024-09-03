from sqlalchemy.orm import Session
from repository.event import EventRepository
from typing import List, Dict


class TriggerService:
    def __init__(self, db: Session):
        self.db = db
        self.event_repository = EventRepository(db)


    def get_event_route(self, event_id: int):
        event = self.event_repository.search_event_by_id(event_id)
        if event:
            return event.route
        return None