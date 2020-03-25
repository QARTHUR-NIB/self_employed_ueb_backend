import os
import urllib.request
from modules.application import app
from flask import Flask, request, redirect, jsonify, send_from_directory
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from werkzeug.utils import secure_filename
import glob

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif','tiff','doc','docx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/multiple-files-upload/<string:app_id>', methods=['POST'])
def upload_file(app_id):
	try:
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