from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from infrastructure.mysql import get_db
from services.auth import get_current_user
from services.trigger_service import TriggerService


router = APIRouter(
    tags=["trigger"], 
    prefix="/trigger"
)


def get_trigger_service(db: Session = Depends(get_db)) -> TriggerService:
    return TriggerService(db)


@router.get("/{event_id}/route")
def get_event_route(event_id: int,
                    user: Annotated[dict, Depends(get_current_user)],
                    service: TriggerService = Depends(get_trigger_service)):
    route = service.get_event_route(event_id)
    if not route:
        raise HTTPException(status_code=404, detail="event or route not found")
    return route


@router.get("/{event_id}/subscribers")
def get_event_subscribers(event_id: int,
                          user: Annotated[dict, Depends(get_current_user)],
                          service: TriggerService = Depends(get_trigger_service)):
    subscribers = service.get_event_subscribers(event_id)
    if not subscribers:
        raise HTTPException(status_code=404, detail="event or subscribers not found")
    return subscribers


@router.get("/{event_id}/{user_id}/content")
def get_event_content(event_id: int,
                      user_id: int,
                      user: Annotated[dict, Depends(get_current_user)],
                      service: TriggerService = Depends(get_trigger_service)):
    
    content = service.get_event_content(event_id=event_id, user_id=user_id)
    if not content:
        raise HTTPException(status_code=404, detail="event or user not found or user not subscribed!")
    return content


@router.get("/{event_id}/notification_data")
def get_event_notification_data(event_id: int,
                                user: Annotated[dict, Depends(get_current_user)],
                                service: TriggerService = Depends(get_trigger_service)):
    notification_data = service.get_event_notification_data(event_id)
    if not notification_data:
        raise HTTPException(status_code=404, detail="Error retriveing notification data")
    return notification_data


@router.get("/{event_id}/email_data_prep")
def prepare_email_data(event_id: int, 
                       user: Annotated[dict, Depends(get_current_user)],
                       service: TriggerService = Depends(get_trigger_service)):
    email_data = service.prepare_email_data(event_id)
    if not email_data:
        raise HTTPException(status_code=401, detail="Error getting email data")
    return email_data


@router.get("/{event_id}/send_notification")
def process_event(event_id: int,
                  user: Annotated[dict, Depends(get_current_user)],
                  service: TriggerService = Depends(get_trigger_service)):
    result = service.process_event(event_id)
    if not result:
        raise HTTPException(status_code=404, detail="Error sending notification")
    return result