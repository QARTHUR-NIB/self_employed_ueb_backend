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

@app.route('/check-run',methods = ["POST"])
@jwt_required
def execute_chk_run():
    try:
        sched.add_job(execute_check_run,id="execute_check_run")
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