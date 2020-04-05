import smtplib
from email.mime.text import MIMEText
from pathlib import Path
import sys
import os
from flask import render_template
import jinja2
from modules.application.background_jobs.mailer import Submission_Email,Employee_Registration_Email,Employer_Registration_Email,\
                                                       Application_Approved_Email,Application_Denied_Email,Payment_Notice_Email,\
                                                       Check_Run_Completed_Email,Check_Run_Aborted_Email,Payment_Notice_Error

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
        elif event == "Check Run Completed":
            env = jinja2.Environment(
                            loader=jinja2.PackageLoader('modules.application','templates')
             )
            template = env.get_template('check_run_completed.html')
            template = template.render()
            check_run_completed_email = Check_Run_Completed_Email.Check_Run_Completed_Email(template)
            check_run_completed_email.send()
        elif event == "Check Run Aborted":
            env = jinja2.Environment(
                            loader=jinja2.PackageLoader('modules.application','templates')
             )
            template = env.get_template('check_run_aborted.html')
            template = template.render(error_message=application)
            check_run_aborted_email = Check_Run_Aborted_Email.Check_Run_Aborted_Email(template)
            check_run_aborted_email.send()
        elif event == "Payment Notice Error":
            env = jinja2.Environment(
                            loader=jinja2.PackageLoader('modules.application','templates')
             )
            template = env.get_template('payment_notice_error.html')
            template = template.render(error_message=application)
            payment_notice_error = Payment_Notice_Error.Payment_Notice_Error(template)
            payment_notice_error.send()