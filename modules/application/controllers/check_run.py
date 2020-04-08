import cx_Oracle
import glob
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from modules.application import app,sched
from config import oraDB
from datetime import datetime
import csv
from modules.application.background_jobs.execute_check_run import execute_check_run
import io

@app.route('/check-run',methods = ["POST"])
@jwt_required
def execute_chk_run():
    try:
        user = get_jwt_identity()
        user = user["user_name"]
        sched.add_job(execute_check_run,id="execute_check_run",args=[user])
        return jsonify(success="Y"),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/check-run',methods = ["GET"])
@jwt_required
def get_check_run_details():
    try:
        data = []                    	
        for file in glob.glob(f"{app.config['EFT_FILES_FOLDER']}\\*.*"):
            data.append({"file_name":os.path.basename(file),
                            "file_type":"EFT",
                            "url":f"/check-run/eft/file/{os.path.basename(file)}"
            })

        for file in glob.glob(f"{app.config['MANUAL_CHECK_FOLDER']}\\*.*"):
            data.append({"file_name":os.path.basename(file),
                            "file_type":"MANUAL",
                            "url":f"/check-run/manual/file/{os.path.basename(file)}"
            })

        return jsonify(success='Y',data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500


@app.route('/check-run/eft/file/<string:file_name>',methods = ["GET"])
def download_eft_file(file_name):
	try:
		return send_from_directory(f"{app.config['EFT_FILES_FOLDER']}",file_name,as_attachment=True)
	except Exception as e:
		return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/check-run/manual/file/<string:file_name>',methods = ["GET"])
def download_manual_file(file_name):
	try:
		return send_from_directory(f"{app.config['MANUAL_CHECK_FOLDER']}",file_name,as_attachment=True)
	except Exception as e:
		return jsonify(success="N",message=f"System Error: {str(e)}"),500

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['csv'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def update_batch_pmt_history(file_stream):
    #load file stream data into csv reader
    csv_input = csv.reader(file_stream)
    #for row in csv_input:

    #loop throguh csv file
    #for each record in file update the check number and the generated flag


@app.route('/check-run/manual/check/check-numbers',methods = ["POST"])
@jwt_required
def update_manual_check_numbers():
    try:
        errors = {}
        success = False
        files = request.files.getlist('file') 
        for file in files:
            if file and allowed_file(file.filename):
                file_stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                update_batch_pmt_history(file_stream)
                filename = secure_filename(file.filename)
                file_stream.seek(0)
            else:
                errors[file.filename] = 'File type is not allowed'
        
        if success and errors:
            errors['message'] = 'File(s) successfully uploaded (partially)'
            resp = jsonify(errors)
            resp.status_code = 400
            return resp
        if success:
            #on successful upload read file and update batch payment history with the check numbers
            resp = jsonify({'message' : 'Files successfully uploaded'})
            resp.status_code = 201
        else:
            resp = jsonify(errors)
            resp.status_code = 400
            return resp
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500