import smtplib
from email.mime.text import MIMEText
from pathlib import Path

class Email:
    def __init__(self,sender,recipient,subject,body):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.body = body
    
    def send(self):
        msg = MIMEText(self.body,"html")
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = self.recipient

        s = smtplib.SMTP('mail.nib-bahamas.com')
        s.sendmail(self.sender, [self.recipient], msg.as_string())
        s.quit()
