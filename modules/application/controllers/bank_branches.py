import cx_Oracle
import os
from flask import Flask, request, jsonify
from modules.application import app
from config import oraDB

@app.route('/bank/branches',methods = ["GET"])
def get_branches():
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\SelfEmployed_UEB\get_bank_branches.sql"
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