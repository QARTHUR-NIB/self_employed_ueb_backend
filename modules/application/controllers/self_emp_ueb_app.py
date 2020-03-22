import cx_Oracle
from flask import Flask, request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from modules.application import app
from config import oraDB
from redis import Redis
from rq import Queue
from modules.application.background_jobs.mailer.Html_Mailer import send_mail
import os

@app.route('/Self-Employed-UEB/application',methods = ["POST"])
def create_application():
    try:
        #q = Queue(connection=Redis())
        email_events = []
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
        account_owner = params["account_owner"]
        branch_number = params["branch_number"]
        account_type = params["account_type"]
        bank_account_number = params["bank_account_number"]
        bank_info_status = params["bank_info_status"]
        cursor.callproc("client.create_self_emp_ueb_app",[first_name,last_name,dob,eeni,\
                        erni,email,primary_contact,secondary_contact,place_of_operation,island_of_operation,\
                        estimated_weekly_earnings,user,account_owner,branch_number,account_type,bank_account_number,\
                        bank_info_status,application_id,success,message])
        if success.getvalue() == "N":
            raise Exception(f"Error Submitting Application: {message.getvalue()}")
        
        if len(eeni) == 0:
            email_events.append("Employee Registration")
        
        if len(erni) == 0:
            email_events.append("Employer Registration")
    
        email_events.append("Application Submitted")
        send_mail(email,email_events,params)
        return jsonify(success='Y',application_id=application_id.getvalue(),message=''),201
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications',methods = ["GET"])
@jwt_required
def get_applications():
    try:
        data = []
        path = ""
        where_clause = ""
        count = 0
        params = request.json
        first_name = request.args["first_name"]
        last_name = request.args["last_name"]
        status = request.args["status"]
        num_filters = 0
        sql = None

        if len(first_name) > 0:
            if num_filters > 0:
                where_clause += f"and upper(first_name) like '%'||upper('{first_name}')||'%' "
            else:
                where_clause = f"where upper(first_name) like '%'||upper('{first_name}')||'%' "
            num_filters+=1
        
        if len(last_name) > 0:
            if num_filters > 0:
                where_clause += f"and upper(last_name) like '%'||upper('{last_name}')||'%' "
            else:
                where_clause = f"where upper(last_name) like '%'||upper('{last_name}')||'%' "
            num_filters+=1
        
        if len(status) > 0:
            if num_filters > 0:
                where_clause += f"and status = '{status}' "
            else:
                where_clause = f"where status = '{status}' "
            num_filters+=1

        if num_filters > 0:
            str_sql = f"select * from(\
                            select app.*,row_number() over (order by app.app_id) rn,\
                            count(app.app_id) over (order by app.app_id) \
                            from client.self_emp_ueb_app app {where_clause}\
                        ) applications\
                        where rn between ((:page_size * :page_number) - (:page_size - 1)) and (:page_size * :page_number)"
        else:
            path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\SelfEmployed_UEB\get_applications.sql"
            sql = open(path,"r")
            str_sql = sql.read()

        params = {"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(str_sql,params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        count = r[18]
                        result = {"application_id":r[0],"first_name":r[1],"last_name":r[2],
                                "dob":r[3],"eeni":r[4],"erni":r[5],
                                "email":r[6],"primary_contact":r[7],"secondary_contact":r[8],
                                "place_of_operation":r[9],"island_of_operation":r[10],
                                "document_location":r[11],"status":r[12],"inserted_by":r[13],
                                "inserted_date":r[14],"updated_by":r[15],"updated_date":r[16],
                                "row_number":r[17],"url":f"/Self-Employed-UEB/applications/{r[0]}"}
                        data.append(result)
        if sql:
            sql.close()
        return jsonify(success="Y",data=data,count=count),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications/<int:app_id>',methods = ["GET"])
@jwt_required
def get_application(app_id):
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\SelfEmployed_UEB\get_individual_applications.sql"
        sql = open(path,"r")
        params = {"app_id":app_id}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        result = {"application_id":r[0],"first_name":r[1],"last_name":r[2],
                                "dob":r[3],"eeni":r[4],"erni":r[5],
                                "email":r[6],"primary_contact":r[7],"secondary_contact":r[8],
                                "place_of_operation":r[9],"island_of_operation":r[10],
                                "estimated_weekly_earnings":r[11],
                                "document_location":r[12],"status":r[13],"inserted_by":r[14],
                                "inserted_date":r[15],"updated_by":r[16],"updated_date":r[17],
                                }
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications/<int:app_id>',methods = ["PUT"])
@jwt_required
def update_application(app_id):
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\SelfEmployed_UEB\update_application.sql"
        sql = open(path,"r")
        user = get_jwt_identity()
        user = user['user_name']
        params = request.json
        params.update([("user_name",user),("app_id",app_id)])
        print(params)
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql.read(),params)
                conn.commit()
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500