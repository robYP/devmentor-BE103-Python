from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from datetime import date, datetime

from infrastructure.mysql import get_db

from services.record import RecordService
from services.scheduler_service import SchedulerService
from services.auth import get_current_user


router = APIRouter(
    tags=["records"],
    prefix="/records"
)


def get_record_service(db: Session = Depends(get_db)) -> RecordService:
    return RecordService(db=db)


def get_scheduler_service(db: Session = Depends(get_db)) -> SchedulerService:
    return SchedulerService(db=db)


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


@router.post("/generate_report/send")
async def send_report(
    user: Annotated[dict, Depends(get_current_user)],
    email: str,
    record_service: RecordService = Depends(get_record_service),
    scheduler_service: SchedulerService = Depends(get_scheduler_service)
):
    if record_service.generate_and_send_report(email=email):
        return {"detail": "Report genearted and sent successfully!"}
    else:
        return {"detail": "Error sending report!"}


@router.get("/jobs")
async def get_jobs(
    user: Annotated[dict, Depends(get_current_user)],
    service: SchedulerService = Depends(get_scheduler_service),
):
    jobs = service.get_jobs()
    return jobs

@router.post("/jobs", status_code=status.HTTP_201_CREATED)
async def add_job(
    id: str,
    user: Annotated[dict, Depends(get_current_user)],
    service: SchedulerService = Depends(get_scheduler_service)
):
    return service.add_job(id=id)

@router.delete("/jobs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    id: str,
    user: Annotated[dict, Depends(get_current_user)],
    service: SchedulerService = Depends(get_scheduler_service)
):
    service.remove_job(id)
    return


@router.post("/schedule_report")
async def schedule_report(
    user: Annotated[dict, Depends(get_current_user)],
    email: str,
    schedule_time: datetime,
    record_service: RecordService = Depends(get_record_service),
    scheduler_service: SchedulerService = Depends(get_scheduler_service)
):
    job = scheduler_service.schedule_report(user.id, email, schedule_time, record_service)
    return {"detail": "Report scheduled successfully", "job_id": job.id}