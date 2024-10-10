import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from config.config import GMAIL_SMTP_SERVER, GMAIL_TLS_PORT, GMAIL_SMTP_USERNAME, GMAIL_SMTP_PASSWORD
import os

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


    def send_email(self, to_email, subject, body, attachments=None):
        try:
            with smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_TLS_PORT) as server:
                server.starttls()
                server.login(GMAIL_SMTP_USERNAME, GMAIL_SMTP_PASSWORD)
                
                msg = MIMEMultipart()
                msg['From'] = GMAIL_SMTP_USERNAME
                msg['To'] = to_email
                msg['Subject'] = subject
                
                msg.attach(MIMEText(body, 'plain'))
                
                if attachments:
                    for attachment in attachments:
                        with open(attachment, 'rb') as file:
                            part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                        msg.attach(part)
                
                server.send_message(msg)
                print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False