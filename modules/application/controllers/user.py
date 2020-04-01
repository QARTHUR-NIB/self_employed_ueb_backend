import cx_Oracle
from config import oraDB
from modules.application import app
from flask import jsonify, request
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_required,jwt_refresh_token_required,get_jwt_identity)
from ldap3 import Server,Connection,ALL,NTLM
import os

@app.route('/user/auth', methods= ['POST'])
def authenticate():
    try:
        data = request.json
        user = data["user_name"]
        pwd = data["password"]
        access_token = ""
        server = Server("172.16.0.6",get_info=ALL)
        conn = Connection(server,user=f"nib-bahamas.com\\{user}",password=pwd,authentication=NTLM,auto_bind=True,raise_exceptions=False)
        conn.open()
        if conn is not None:
            success = 'Y'
            access_token = create_access_token(identity=data)             
        
        return jsonify(success=success,token=access_token,message=""),200
    except Exception as e:
        if str(e) == 'None':
            success = 'N'
            message = "Invalid Credentials"
            return jsonify(success=success,token=access_token,message=message),404
        else:
            return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/auth/user', methods= ['GET'])
@jwt_required
def authenticated_user():
    try:
        user = get_jwt_identity()
        user_object = None
        data = []
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_current_user_role.sql")
        sql = open(path,"r")
        params = {"user_name":user['user_name']}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        user_object = {"user_name":r[0],"user_group":r[1]}    
        sql.close()
        return jsonify(success="Y",user=user_object),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/user/groups', methods= ['GET'])
def get_user_V3_roles():
    try:
        data = []
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_user_groups.sql")
        sql = open(path,"r")
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