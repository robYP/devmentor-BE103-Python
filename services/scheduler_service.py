from sqlalchemy.orm import Session
from fastapi import Depends
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime
from infrastructure.mysql import get_db

from sqlalchemy.orm import sessionmaker
from infrastructure.mysql import engine  # Import the engine to create sessions


def generate_and_send_report(email: str, db: Session = Depends(get_db)):
    from services.record import RecordService  # Avoid circular import issues
    record_service = RecordService(db)
    record_service.generate_and_send_report(email)
    print(f"Report sent to {email}")




def job(id: str = "No id"):
    print(
            f"time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Work: {id} I'm working..."
    )
    

class SchedulerService:
    def __init__(self, db:Session):
        jobstores = {
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        }
        executors = {
            'default': ThreadPoolExecutor(20)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        self.scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
        self.scheduler.start()
        self.db = db

   
    def get_jobs(self):
        jobs = self.scheduler.get_jobs()
        if not jobs:
            return []
    
        job_list = []
        
        for job in jobs:
            try:
                job_data = {
                    "id": job.id,  
                    "next_run_time": job.next_run_time if job.next_run_time else "N/A"
                }
            except AttributeError as e:
                print(f"Error accessing job attributes: {e}")
                job_data = {
                    "id": "Unknown",
                    "next_run_time": "N/A"
                }
            
            job_list.append(job_data)
        
        return job_list
    
    def add_job(self, id: str):
        self.scheduler.add_job(job, "interval", seconds=5, id=id, args=[id])
        return {"message": "job added"}
    
    
    def remove_job(self, id: str):
        self.scheduler.remove_job(id)
        return
    
    
    def schedule_report(self, user_id: int, email: str, schedule_time: datetime, record_service):
        # print("*******************")
        # print(type(generate_and_send_report))
        # print(f"{schedule_time}") 
        # print(f"{datetime.now()}")
        # schedule_time1 = schedule_time.strftime('%Y-%m-%d %H:%M:%S')
        # schedule_time2 = datetime.now()
        # print(f"{schedule_time1}")
        job = self.scheduler.add_job(
            func = generate_and_send_report,
            trigger = 'interval',
            # run_date=schedule_time,
            seconds=10,
            args=[email],
            id=f"send_report_{user_id}",
        )
        return job
    
    
    # @staticmethod
    # def generate_and_send_report(db: Session, email: str):
    #     from services.record import RecordService  # Import here to avoid circular imports
    #     record_service = RecordService(db)
    #     return record_service.generate_and_send_report(email)
    
    