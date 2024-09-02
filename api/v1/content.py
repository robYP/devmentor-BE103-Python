from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from infrastructure.mysql import get_db
from schema.database.event import EventCreate
from services.auth import get_current_user

from services.event_service import EventService
from services.event_user_service import EventUserService

from services.content import ContentService
from schema.database.content import ContentCreate, Content

router = APIRouter(
    tags=["contents"],
    prefix="/contents"
)


def get_content_service(db: Session = Depends(get_db)) -> ContentService:
    return ContentService(db=db)


@router.get("/")
def list_contents_by_event(
    event_id:int, 
    user: Annotated[dict, Depends(get_current_user)],
    service: ContentService = Depends(get_content_service)
):
    return service.list_contents_by_event(event_id=event_id)


@router.post("/")
def create_content(
    content: ContentCreate,
    user: Annotated[dict, Depends(get_current_user)],
    service: ContentService = Depends(get_content_service)
):
    created_event = service.create_content(user=user, content=content)
    if not created_event:
        raise HTTPException(status_code=400, detail="Event ID not found or content already exisits")
    return created_event


@router.put("/")
def update_content(
    content: ContentCreate,
    user: Annotated[dict, Depends(get_current_user)],
    service: ContentService = Depends(get_content_service)
):
    updated_content = service.update_content(content=content, user=user)
    if not updated_content:
        raise HTTPException(status_code=400, detail="Event_id or Content not found")
    return updated_content


@router.delete("/")
def delete_content(
    event_id: int,
    language: str,
    user: Annotated[dict, Depends(get_current_user)],
    service: ContentService = Depends(get_content_service)
):
    deleted_content = service.delete_content(event_id=event_id, language=language, user=user)
    if not deleted_content:
        raise HTTPException(status_code=404, detail="Event_id or Content not found")
    return deleted_content