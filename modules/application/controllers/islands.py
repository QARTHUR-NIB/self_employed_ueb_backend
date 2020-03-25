import cx_Oracle
import os
from flask import Flask, request, jsonify
from modules.application import app
from config import oraDB

@app.route('/islands',methods = ["GET"])
def get_islands():
    try:
        data = []
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_islands.sql")
        sql = open(path,"r")
        #params = {"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read())
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        data.append(r[0])
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500