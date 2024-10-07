from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from infrastructure.mysql import get_db

from services.record import RecordService
from services.auth import get_current_user


router = APIRouter(
    tags=["records"],
    prefix="/records"
)

def get_record_service(db: Session = Depends(get_db)) -> RecordService:
    return RecordService(db=db)

@router.get("/")
def list_records(
    skip: int = 0, 
    limit: int = 100,
    service: RecordService = Depends(get_record_service)
):
    
    return service.list_records(skip=skip, limit=limit)

