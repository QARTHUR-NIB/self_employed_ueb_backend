import cx_Oracle
import os
from flask import Flask, request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from modules.application import app
from config import oraDB
from modules.application.background_jobs.notify_applicants_of_payments import send_notice_to_all_paid_applicants

@app.route('/Self-Employed-UEB/applications/<int:app_id>/payments',methods = ["GET"])
@jwt_required
def get_payments(app_id):
    try:
        data = []
        #path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\SelfEmployed_UEB\get_payment_master.sql"
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_payment_master.sql")
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
                        result = {"pmt_id":r[0],"pmt_date":r[1],"pmt_type":r[2],
                                "pmt_amt":r[3],"beg_pay_period":r[4],"end_pay_period":r[5],
                                "pmt_status":r[6],"pmt_updated_by":r[7],"updated_date":r[8],
                                "url":f"/Self-Employed-UEB/applications/{app_id}/payments/{r[0]}/details"}
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications/<int:app_id>/payments/<int:pmt_id>/details',methods = ["GET"])
@jwt_required
def get_payment_details(app_id,pmt_id):
    try:
        data = []
        #path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\SelfEmployed_UEB\get_payment_details.sql"
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_payment_details.sql")
        sql = open(path,"r")
        params = {"app_id":app_id,"pmt_id":pmt_id}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        result = {"pmt_det_id":r[0],"pmt_id":r[1],"beg_pay_period":r[2],"end_pay_period":r[3],
                                   "assistance_amt":r[4],"benefit_penalty_amount":r[5],"pmt_amt":r[6]
                                 }
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications/<int:app_id>/payments/<int:pmt_id>/status',methods = ["PUT"])
@jwt_required
def update_payment_status(app_id,pmt_id):
    try:
        data = []
        params =  request.json
        if params["status"] not in ['Voided','Reissued']:
            raise Exception("Invalid status only ('Pending','Paid','Voided','Reissued') allowed")

        #path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\SelfEmployed_UEB\update_payment_status.sql"
        path = os.path.join(app.config['SCRIPT_FOLDER'],"update_payment_status.sql")
        sql = open(path,"r")
        user = get_jwt_identity()
        user = user['user_name']
        params.update([("app_id",app_id),("pmt_id",pmt_id),("user_name",user)])
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
          with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql.read(),params)
                conn.commit()
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications/<int:app_id>/payments/summary',methods = ["GET"])
@jwt_required
def get_payment_summary(app_id):
    try:
        data = []
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_payment_summary.sql")
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
                        result = {"tot_amt_paid":r[1],"tot_weeks_paid":r[2]
                                 }
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

