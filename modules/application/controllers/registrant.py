import cx_Oracle
import os
from flask import Flask, request, jsonify
from modules.application import app
from config import oraDB

@app.route('/person/<string:eeni>',methods = ["GET"])
def get_reg(eeni):
    try:
        res = None
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\SelfEmployed_UEB\validate_reg_nib#.sql"
        sql = open(path,"r")
        params = {"eeni#":eeni}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        res = r[0]
                if res is None:
                    res = 'N'
                else:
                    res = 'Y'
        sql.close()
        return jsonify(success="Y",exists=res),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500