import cx_Oracle
from flask import Flask, request, jsonify
from modules.application import app
from config import oraDB
from redis import Redis
from rq import Queue
from modules.application.background_jobs.mailer.mailer import send_mail
import os

@app.route('/Self-Employed-UEB/application',methods = ["POST"])
def create_application():
    try:
        q = Queue(connection=Redis())
        conn = cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}")
        cursor = conn.cursor()
        application_id = cursor.var(cx_Oracle.NUMBER,20) if not None else ''
        success = cursor.var(cx_Oracle.STRING,1) if not None else ''
        message = cursor.var(cx_Oracle.STRING,250) if not None else ''
        params = request.json
        first_name = params["first_name"]
        last_name = params["last_name"]
        dob = params["dob"]
        eeni = params["eeni"]
        erni = params["erni"]
        email = params["email"]
        primary_contact = params["primary_contact"]
        secondary_contact = params["secondary_contact"]
        place_of_operation = params["place_of_operation"]
        island_of_operation = params["island_of_operation"]
        estimated_weekly_earnings = params["estimated_weekly_earnings"]
        user = 'SYSTEM'
        branch_number = params["branch_number"]
        bank_code = params["bank_code"]
        account_type = params["account_type"]
        bank_account_number = params["bank_account_number"]
        bank_info_status = params["bank_info_status"]
        cursor.callproc("client.create_self_emp_ueb_app",[first_name,last_name,dob,eeni,\
                        erni,email,primary_contact,secondary_contact,place_of_operation,island_of_operation,\
                        estimated_weekly_earnings,user,branch_number,bank_code,account_type,bank_account_number,\
                        bank_info_status,application_id,success,message])
        if success.getvalue() == "N":
            raise Exception(f"Error Submitting Application: {message.getvalue()}")
        
        subject = "Self Employed Unemployment Benefit Assistance"
        sender = "claims@nib-bahamas.com"
        template_path =  os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/background_jobs/mailer/html_templates/app_submitted.hmtl"
        res = q.enqueue(send_mail,subject,sender,email,template_path)
        return jsonify(success='Y',message=''),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500