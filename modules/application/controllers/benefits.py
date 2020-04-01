import cx_Oracle
import os
from flask import Flask, request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from modules.application import app
from config import oraDB

@app.route('/Self-Employed-UEB/applications/<int:app_id>/benefits',methods = ["GET"])
@jwt_required
def get_applicant_nib_benefits(app_id):
    try:
        data = []
        params = {"app_id":app_id}
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_applicant_benefit.sql")
        sql = open(path,"r")
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        data.append({"benefit_type":r[1]})
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500