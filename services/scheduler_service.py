from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime


def job(id: str = "No id"):
    print(
            f"time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Work: {id} I'm working..."
    )

class SchedulerService:
    def __init__(self):
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

   
    def get_jobs(self):
        jobs = self.scheduler.get_jobs()
        if not jobs:
            return []
    
        job_list = []
        
        for job in jobs:
            # Debugging: Check the type and attributes of the job
            print(f"Type of job: {type(job)}")
            print(f"Job object: {job}")
            
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
    
    
    def test_schedule(self):
        print("THis is the test_schedule")
        job = self.scheduler.add_job(
            self.job,
            "interval",
            seconds=5,
            
        )
        return job