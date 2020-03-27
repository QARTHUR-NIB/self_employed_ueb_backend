import cx_Oracle
from config import oraDB
import os
import urllib.request
from modules.application import app
from flask import Flask, request, redirect, jsonify, send_from_directory
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from werkzeug.utils import secure_filename
import glob
from modules.application.background_jobs.mailer.Html_Mailer import send_mail
 
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif','tiff','doc','docx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/multiple-files-upload/<string:app_id>', methods=['POST'])
def upload_file(app_id):
	try:
		email_events = []
		files = request.files.getlist('file')
			
		errors = {}
		success = False
		
		for file in files:
			print(file)		
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)

				if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],app_id)):
					os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],app_id))
				
				if not os.path.exists(os.path.join(f"{app.config['UPLOAD_FOLDER']}\\{app_id}\\", filename)):
					file.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}\\{app_id}\\", filename))
					success = True
				else:
					success = True
			else:
				errors[file.filename] = 'File type is not allowed' 
		
		if success and errors:
			errors['message'] = 'File(s) successfully uploaded'
			resp = jsonify(errors)
			resp.status_code = 500
			return resp
		if success:
			resp = jsonify({'message' : 'Files successfully uploaded'})
			resp.status_code = 201

			user = None
			path = os.path.join(app.config['SCRIPT_FOLDER'],"get_individual_applications.sql")
			sql = open(path,"r")
			params = {"app_id":app_id}
			with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
				with conn.cursor() as cursor:
					results = cursor.execute(sql.read(),params)
					while True:
						rows = results.fetchall()
						if not rows:
							break
						for r in rows:
							user = {"application_id":r[0],"first_name":r[1],"last_name":r[2],
									"dob":r[3],"eeni":r[4],"erni":r[5],
									"email":r[6],"primary_contact":r[7],"secondary_contact":r[8],
									"place_of_operation":r[9],"island_of_operation":r[10],
									"estimated_weekly_earnings":r[11],"status":r[13],"approval_date":r[14],
									"inserted_by":r[15],
									"inserted_date":r[16],"updated_by":r[17],"updated_date":r[18],
									"approved_by":r[19],"denied_by":r[20],"comment":r[21],
									"denial_date":r[22],"nature_of_employment":r[23],
									"url":f"/Self-Employed-UEB/applications/{r[0]}"}
			sql.close()
					 
			if len(user["eeni"]) == 0:
				email_events.append("Employee Registration")
			
			if len(user["erni"]) == 0:
				email_events.append("Employer Registration")
		
			email_events.append("Application Submitted")
			send_mail(email_events,user)

			return resp

		else:
			resp = jsonify(errors)
			resp.status_code = 500
			return resp
	except FileExistsError as e:
		return jsonify(success="N",message=f"File already exists"),500
	except Exception as e:
		return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/uploads/<string:app_id>',methods = ["GET"])
@jwt_required
def get_uploaded_files(app_id):
	try:
		data = []		
		for file in glob.glob(f"{app.config['UPLOAD_FOLDER']}\\{app_id}\\*.*"):
			data.append({"file_name":os.path.basename(file),
			  			  "url":f"/uploads/{app_id}/file/{os.path.basename(file)}"
			})
		return jsonify(success="Y",data=data),200
	except Exception as e:
		return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/uploads/<string:app_id>/file/<string:file_name>',methods = ["GET"])
def download_file(app_id,file_name):
	try:
		return send_from_directory(f"{app.config['UPLOAD_FOLDER']}\\{app_id}",file_name,as_attachment=True)
	except Exception as e:
		return jsonify(success="N",message=f"System Error: {str(e)}"),500