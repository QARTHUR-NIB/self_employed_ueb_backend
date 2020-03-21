import os
import urllib.request
from modules.application import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename

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
				
				if not os.path.exists(os.path.join(f"{app.config['UPLOAD_FOLDER']}/{app_id}/", filename)):
					file.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}/{app_id}/", filename))
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