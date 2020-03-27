import cx_Oracle
import os
from flask import Flask, request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from modules.application import app
from config import oraDB
from datetime import datetime

@app.route('/check-run',methods = ["POST"])
@jwt_required
def execute_check_run():
    try:
        conn = cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}")
        cursor = conn.cursor()
        success = cursor.var(cx_Oracle.STRING,1) if not None else ''
        message = cursor.var(cx_Oracle.STRING,250) if not None else ''

        cursor.callproc("client.execute_se_ueb_check_run",[success,message])

        if success.getvalue() == "N":
            raise Exception(f"Error Initiating Check Run: {message.getvalue()}")

        return jsonify(success="Y"),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/check-run/status',methods = ["GET"])
@jwt_required
def get_check_run_status():
    try:
        status = ""
        completed = False
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_check_run_status.sql")
        sql = open(path,"r")
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read())
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        status = r[0]

        if status in ['JOB_SUCCEEDED','JOB_COMPLETED']:
            completed = True
        
        sql.close()
        return jsonify(success='Y',completed=completed),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/check-run',methods = ["GET"])
@jwt_required
def get_check_run_details():
    try:
        status = ""
        completed = False
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_pending_reissued_payments.sql")
        sql = open(path,"r")
        file_header = None
        batch_header = None
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read())
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    #write file header
                    file_header = f"101 0056250030000000000{datetime.today().strftime('%y%m%d')}{datetime.today().strftime('%I%M')}1094101Royal Bank of Canada"\
                                  "   National Insurance             "
                    batch_header = f"5220NIB             Long Term Benefits  0002883221PPDClaims    {datetime.today().strftime('%y%m%d')}{datetime.today().strftime('%y%m%d')}"\
                                  "0001056250030000001"
                    print(file_header)
                    print(batch_header)
                    for r in rows:
                        pmt_record = f"{r[0]}{r[1]}{r[2]}{r[3]}{r[4]:<17}{r[5]:010}{r[6]:<15}{r[7]:<22}{r[8]}{r[9]:06}"
                        print(pmt_record)

                    #batch_control = f"8220{count:06}"


        if status in ['JOB_SUCCEEDED','JOB_COMPLETED']:
            completed = True
        
        sql.close()
        return jsonify(success='Y',completed=completed),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500