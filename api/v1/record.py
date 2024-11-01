from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from datetime import date

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


@router.get("/generate_report")
async def generate_report(
    user: Annotated[dict, Depends(get_current_user)],
    service: RecordService = Depends(get_record_service),
    report_date: Annotated[Optional[date], Query(description="Optional report date in YYYY-MM-DD format")] = None
):
    report = service.generate_event_distribution_report(report_date=report_date)
    
    if report is None:
        raise HTTPException(status_code=404, detail="Report Not Generated")
    
    return {"detail": "Report successfully generated", "report_path": report}
