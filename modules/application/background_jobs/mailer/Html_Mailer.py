import smtplib
from email.mime.text import MIMEText
from pathlib import Path
import sys
import os
from flask import render_template
from modules.application.background_jobs.mailer import Submission_Email,Employee_Registration_Email,Employer_Registration_Email

def send_mail(recipient,email_events,application):
     for event in email_events:
        if event == "Application Submitted":
            template = render_template('app_submitted.html',application=application)
            sub_email = Submission_Email.Submission_Email(application["email"],template)
            sub_email.send()
        elif event == "Employee Registration":
            template = render_template('employee_registration.html',application=application)
            eeni_reg_email = Employee_Registration_Email.Employee_Registration_Email(template)
            eeni_reg_email.send()
        elif event == "Employer Registration":
            template = render_template('employer_registration.html',application=application)
            erni_reg_email = Employer_Registration_Email.Employer_Registration_Email(template)
            erni_reg_email.send()