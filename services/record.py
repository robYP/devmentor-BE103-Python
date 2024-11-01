from sqlalchemy.orm import Session
from repository.record import RecordRepository
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from services.email_service import EmailService 

class RecordService:
    def __init__(self, db: Session):
        self.record_repository = RecordRepository(db)
        self.email_service = EmailService()
        
    
    def list_records(self, skip: int=0, limit:int=100):
        records = self.record_repository.list_records(skip=skip, limit=limit)
        return records

    def generate_event_distribution_report(self, report_date: date = None):
        records = self.record_repository.list_records()
        
        # Convert the list of SQLAlchemy ORM objects to a list of dictionaries
        if records:
            records_dicts = [
                {
                    'created_at': record.created_at,
                    'event_name': record.event_name,
                    'user_id': record.user_id,
                    'event_id': record.event_id,
                    'action': record.action
                } 
                for record in records
            ]
        else:
            records_dicts = []
        
        df = pd.DataFrame(records_dicts)
        df_create_event = df[df['action'] == 'Create Event']
        
        # Ensure 'created_at' is in datetime format
        df_create_event['created_at'] = pd.to_datetime(df['created_at'])

        if report_date is None:
            report_date = date.today()
            
        # Extract the date part and filter for the specific day
        df['date'] = df['created_at'].dt.date
        df_create_event = df[(df['action'] == 'Create Event') & (df['date'] == report_date)]
        
        # Extract the hour part from 'created_at'
        df_create_event['hour'] = df_create_event['created_at'].dt.hour

        # Group data by hour and event name for analysis
        event_hourly_distribution = df_create_event.groupby(['hour', 'event_name']).size().unstack(fill_value=0)

        plt.figure(figsize=(14, 6))
        event_hourly_distribution.plot(ax=plt.gca())
        plt.title(f'Event Distribution by Time of Day (Create Events) on {report_date}')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Events')
        plt.legend(title='Event Name')

        plot_path = f'event_distribution_create_events_{report_date}.png'
        plt.savefig(plot_path)
        plt.close()
        
        return plot_path
    
    
    def generate_and_send_report(self, email: str):
        report_path = self.generate_event_distribution_report()
        
        if report_path:
            subject = "Event Distribution Report"
            body = "Please find attached the event distribution report."
            self.email_service.send_email(email, subject, body, [report_path])
            return True
        return False