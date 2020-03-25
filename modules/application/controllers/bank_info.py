import cx_Oracle
import os
from flask import Flask, request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from modules.application import app
from config import oraDB

@app.route('/bank/branches',methods = ["GET"])
def get_branches():
    try:
        data = []
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_bank_branches.sql")
        sql = open(path,"r")
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read())
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        data.append(r)
                        
        sql.close()
        return jsonify(success="Y",branches=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications/<int:app_id>/banking-info',methods = ["GET"])
@jwt_required
def get_bank_account_info(app_id):
    try:
        data = []
        params = {"app_id":app_id}
        #path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\SelfEmployed_UEB\get_bank_info.sql"
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_bank_info.sql")
        sql = open(path,"r")
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        data.append({"branch_number":r[2],"account_type":r[3],
                                     "bank_account_number":r[4],"account_owner":r[5],
                                     "status":r[6],"inserted_by":r[7],"inserted_date":r[8]})     
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/Self-Employed-UEB/applications/<int:app_id>/banking-info',methods = ["POST"])
@jwt_required
def create_bank_account_info(app_id):
    try:
        conn = cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}")
        cursor = conn.cursor()
        params = request.json
        success = cursor.var(cx_Oracle.STRING,1) if not None else ''
        message = cursor.var(cx_Oracle.STRING,250) if not None else ''
        app_id = app_id
        account_owner = params["account_owner"]
        branch_number = params["branch_number"]
        account_type = params["account_type"]
        bank_account_number = params["bank_account_number"]
        bank_info_status = 'Active'
        user = get_jwt_identity()
        user = user['user_name']
        cursor.callproc("client.create_se_ueb_app_bank_info",[app_id,\
                        branch_number,account_type,bank_account_number,bank_info_status,\
                        account_owner,user,success,message])

        if success.getvalue() == "N":
            raise Exception(f"Error Creating Bank Account {message.getvalue()}")

        return jsonify(success='Y',message=''),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500