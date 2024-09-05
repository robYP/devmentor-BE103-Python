import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import GMAIL_SMTP_SERVER, GMAIL_TLS_PORT, GMAIL_SMTP_USERNAME, GMAIL_SMTP_PASSWORD

class EmailService:
    def send_emails(self, email_data_list) -> bool :
        try:
            with smtplib.SMTP(GMAIL_SMTP_SERVER) as connection:
                connection.starttls()
                connection.login(user=GMAIL_SMTP_USERNAME, password=GMAIL_SMTP_PASSWORD)
                
                for email_data in email_data_list:
                    if not email_data:
                        continue
                    
                    msg = MIMEMultipart()
                    msg["From"] = GMAIL_SMTP_USERNAME
                    msg["To"] = email_data["To"]
                    msg["Subject"] = email_data["Subject"]
                    
                    body = email_data["body"]
                    msg.attach(MIMEText(body, "plain"))
                    
                    connection.send_message(msg)
                    print(f"Email sent to {email_data['To']}")
            return True
        except Exception as e:
            print(f"Error sending emails: {str(e)}")
            return False
            