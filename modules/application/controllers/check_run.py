import cx_Oracle
import os
from flask import Flask, request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from modules.application import app
from config import oraDB

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