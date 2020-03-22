from modules.application import app
from flask import jsonify, request
from flask_jwt_extended import (create_access_token,create_refresh_token,jwt_required,jwt_required,jwt_refresh_token_required,get_jwt_identity)
from ldap3 import Server,Connection,ALL,NTLM

@app.route('/user/auth', methods= ['POST'])
def authenticate():
    try:
        data = request.json
        user = data["user_name"]
        pwd = data["password"]
        access_token = ""
        server = Server("nib-bahamas.com",get_info=ALL)
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
        user = user['user_name']
        return jsonify(success='Y',user=user,message=""),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500