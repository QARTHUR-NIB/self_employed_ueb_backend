import smtplib
from email.mime.text import MIMEText
from pathlib import Path
import sys
import os
from flask import render_template
import jinja2
from modules.application.background_jobs.mailer import Submission_Email,Employee_Registration_Email,Employer_Registration_Email,\
                                                       Application_Approved_Email,Application_Denied_Email,Payment_Notice_Email

def send_mail(email_events,application):
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
        elif event == "Application Approved":
            template = render_template('app_approved.html',application=application)
            app_aprv_email = Application_Approved_Email.Application_Approved_Email(application["email"],template)
            app_aprv_email.send()
        elif event == "Application Denied":
            template = render_template('app_denied.html',application=application)
            app_aprv_email = Application_Denied_Email.Application_Denied_Email(application["email"],template)
            app_aprv_email.send()
        elif event == "Payment Generated":
            #becuse payments are generated in a sperate process cannot use flask templating engine
            env = jinja2.Environment(
                            loader=jinja2.PackageLoader('modules.application','templates')
             )
            template = env.get_template('payment_notice.html')
            template = template.render(application=application)
            pmt_notice_email = Payment_Notice_Email.Payment_Notice_Email(application["email"],template)
            pmt_notice_email.send()