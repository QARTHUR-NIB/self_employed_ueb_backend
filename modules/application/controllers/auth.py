import cx_Oracle
import os
from flask import Flask, request, jsonify
from modules.application import app
from config import oraDB

@app.route('/auth',methods = ["POST"])
def get_inspector_unit_area():
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\Compliance Scripts\Data Migration\Get_Inspector_Unit_Area.sql"
        sql = open(path,"r")
        params = {"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        data.append(r)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500