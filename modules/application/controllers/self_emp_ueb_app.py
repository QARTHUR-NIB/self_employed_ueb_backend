import cx_Oracle
from flask import Flask, request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from modules.application import app
from config import oraDB
import os
from modules.application.background_jobs.mailer.Html_Mailer import send_mail

@app.route('/Self-Employed-UEB/application',methods = ["POST"])
def create_application():
    try: 
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
        bank_info_exists = params["bank_info_exists"]
        nature_of_employment = params["nature_of_employment"]
        cursor.callproc("client.create_self_emp_ueb_app",[first_name,last_name,dob,eeni,\
                        erni,email,primary_contact,secondary_contact,place_of_operation,island_of_operation,\
                        estimated_weekly_earnings,user,account_owner,branch_number,account_type,bank_account_number,\
                        bank_info_status,bank_info_exists,nature_of_employment,application_id,success,message])

        if success.getvalue() == "N":
            raise Exception(f"Error Submitting Application: {message.getvalue()}")
       
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
        params = request.args
        first_name = request.args["first_name"]
        last_name = request.args["last_name"]
        status = request.args["status"]
        routed_to = request.args['routed_to']
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
        
        if len(routed_to) > 0:
            if num_filters > 0:
                where_clause += f"and upper(routed_to) like '%'||upper('{routed_to}')||'%' "
            else:
                where_clause = f"where upper(routed_to) like '%'||upper('{routed_to}')||'%' "
                num_filters+=1

        if num_filters > 0:
            str_sql = f"select * from(\
                            select app.*,row_number() over (order by app.app_id) rn,\
                            count(*) over () \
                            from client.self_emp_ueb_app app {where_clause}\
                        ) applications\
                        where rn between ((:page_size * :page_number) - (:page_size - 1)) and (:page_size * :page_number)"
        else:
            path = os.path.join(app.config['SCRIPT_FOLDER'],"get_applications.sql")
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
                        count = r[29]
                        result = {"application_id":r[0],"first_name":r[1],"last_name":r[2],
                                "dob":r[3],"eeni":r[4],"erni":r[5],
                                "email":r[6],"primary_contact":r[7],"secondary_contact":r[8],
                                "place_of_operation":r[9],"island_of_operation":r[10],
                                "estimated_weekly_earnings":r[11],"status":r[13],"approval_date":r[14],
                                "inserted_by":r[15],
                                "inserted_date":r[16],"updated_by":r[17],"updated_date":r[18],
                                "approved_by":r[19],"denied_by":r[20],"comment":r[21],
                                "denial_date":r[22],"nature_of_employment":r[23],"routed_to":r[24],
                                "routed_date":r[25],"tourism_industry":r[26],"sun_cash_opt_in":r[27],"row_number":r[28],"url":f"/Self-Employed-UEB/applications/{r[0]}"}
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
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_individual_applications.sql")
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
                                "estimated_weekly_earnings":r[11],"status":r[13],"approval_date":r[14],
                                "inserted_by":r[15],
                                "inserted_date":r[16],"updated_by":r[17],"updated_date":r[18],
                                "approved_by":r[19],"denied_by":r[20],"comment":r[21],
                                "denial_date":r[22],"nature_of_employment":r[23],"routed_to":r[24],
                                "routed_date":r[25],"sun_cash_opt_in":r[26],"tourism_industry":r[27],"url":f"/Self-Employed-UEB/applications/{r[0]}"}
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications/<int:app_id>',methods = ["PUT"])
@jwt_required
def update_application(app_id):
    try:
        params = request.json
        first_name = params["first_name"]
        last_name = params["last_name"]
        dob = params["dob"]
        eeni = params["eeni"]
        email = params["email"]
        primary_contact = params["primary_contact"]
        secondary_contact = params["secondary_contact"]
        user_comment =  params["user_comment"]
        user_name = get_jwt_identity()
        user_name = user_name["user_name"]
        missing_nib = params["missing_nib"]
        tourism_industry = params["tourism_industry"]
        sun_cash_opt_in = params["sun_cash_opt_in"]
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                success = cursor.var(cx_Oracle.STRING,1) if not None else ''
                message = cursor.var(cx_Oracle.STRING,250) if not None else ''
                cursor.callproc("client.update_se_ueb_apps",[app_id,first_name,last_name,dob,eeni,\
                                 email,primary_contact,secondary_contact,user_comment,user_name,missing_nib,tourism_industry,sun_cash_opt_in,success,message])

        if success.getvalue() == "N":
            raise Exception(f"Error Updating Application: {message.getvalue()}")
       
        return jsonify(success='Y',message=''),201
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications/<int:app_id>/status',methods = ["PUT"])
@jwt_required
def update_application_status(app_id):
    try:
        data = []
        email_events = []
        path = ""
        params = request.json

        if params["status"] == 'Approved':
            user_app = params.get('application')
            user_app["comment"] = params["user_comment"]
            path = os.path.join(app.config['SCRIPT_FOLDER'],"approve_application.sql")
            email_events.append("Application Approved")
        elif params["status"] == 'Denied':
            user_app = params.get('application')
            user_app["comment"] = params["user_comment"]
            path = os.path.join(app.config['SCRIPT_FOLDER'],"deny_application.sql")
            email_events.append("Application Denied")
        elif params["status"] == 'Pending':
            del params['user_comment'] #remove because this field is not needed in override script
            path = os.path.join(app.config['SCRIPT_FOLDER'],"override_application_status.sql")
        else:
            raise Exception("Invalid Status only ['Pending','Approved','Denied'] permitted")
        
        del params['application'] #remove application because oracle cannot not parse dictionary data
        sql = open(path,"r")
        user = get_jwt_identity()
        user = user['user_name']
        params.update([("user_name",user),("app_id",app_id)])
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql.read(),params)
                conn.commit()
        sql.close() 

        if params['status'] not in ['Pending']:
            send_mail(email_events,user_app)
        
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications/<int:app_id>',methods = ["DELETE"])
def delete_application_status(app_id):
    try:
        conn = cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}")
        cursor = conn.cursor()
        success = cursor.var(cx_Oracle.STRING,1) if not None else ''
        message = cursor.var(cx_Oracle.STRING,250) if not None else ''
        cursor.callproc("client.delete_self_emp_ueb_app",[app_id,success,message])
        if success.getvalue() == "N":
            raise Exception(f"Error Deleting Application: {message.getvalue()}")

        return jsonify(success="Y",message=""),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications/<int:app_id>/owner',methods = ["POST"])
@jwt_required
def route_application_to_user(app_id):
    try:
        user = get_jwt_identity()
        user = user["user_name"]
        conn = cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}")
        cursor = conn.cursor()
        success = cursor.var(cx_Oracle.STRING,1) if not None else ''
        message = cursor.var(cx_Oracle.STRING,250) if not None else ''
        cursor.callproc("client.self_emp_ueb_route_app_to_me",[app_id,user,success,message])
        if success.getvalue() == "N":
            raise Exception(f"Error Routing Application: {message.getvalue()}")

        return jsonify(success="Y",message=message.getvalue()),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/test/email')
def test_email():
    email_events = []
    user_app = "test"
    email_events.append("Check Run Aborted")
    send_mail(email_events,user_app)
    return jsonify("Test Email Send Successfully"), 200