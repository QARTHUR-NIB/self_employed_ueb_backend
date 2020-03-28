import cx_Oracle
import glob
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from modules.application import app
from config import oraDB
from datetime import datetime

@app.route('/check-run',methods = ["POST"])
@jwt_required
def execute_check_run():
    try:
        conn = cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}")
        cursor = conn.cursor()
        success = cursor.var(cx_Oracle.STRING,1) if not None else ''
        message = cursor.var(cx_Oracle.STRING,250) if not None else ''

        cursor.callproc("client.execute_se_ueb_check_run",[success,message])

        if success.getvalue() == "N":
            raise Exception(f"Error Initiating Check Run: {message.getvalue()}")

        return jsonify(success="Y"),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/check-run/status',methods = ["GET"])
@jwt_required
def get_check_run_status():
    try:
        status = ""
        completed = False
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_check_run_status.sql")
        sql = open(path,"r")
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read())
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        status = r[0]

        if status in ['JOB_SUCCEEDED','JOB_COMPLETED']:
            completed = True
        
        sql.close()
        return jsonify(success='Y',completed=completed),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

def write_file(file_path,line):
    try:         
        with open(file_path,'a') as check_file:
            print(line)
            check_file.write(line)
            check_file.write("\n")
        #logger = csv.writer(log_file,delimiter=",",quotechar='"',quoting=csv.QUOTE_MINIMAL)
        #logger.writerow(tuple(row))
    except Exception as e:
        print(f"Error writing exception file: {str(e)}")

@app.route('/check-run',methods = ["GET"])
@jwt_required
def get_check_run_details():
    try:
        data = []	
        path = os.path.join(app.config['SCRIPT_FOLDER'],"get_eft_pending_payments.sql")
        sql = open(path,"r")
        file_header = None
        batch_header = None
        count = 0
        block_count = 0
        entry_hash = 0
        total_credit = 0
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read())
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    #Write EFT File(Nacha File Format)    
                    file_name = f"SE_UEB_EFT_{datetime.today().strftime('%Y-%m-%d-%I%M')}.txt"
                    file_path = os.path.join(app.config['EFT_FILES_FOLDER'],file_name)
                    file_header = f"101 0056250030000000000{datetime.today().strftime('%y%m%d')}{datetime.today().strftime('%I%M')}1094101Royal Bank of Canada"\
                                  "   National Insurance             "
                    write_file(file_path,file_header)
                    batch_header = f"5220NIB             Long Term Benefits  0002883221PPDClaims    {datetime.today().strftime('%y%m%d')}{datetime.today().strftime('%y%m%d')}"\
                                  "0001056250030000001"
                    write_file(file_path,batch_header)
                    count =  len(rows)
                    if (count + 4) % 10 == 0:
                        block_count = int((count + 4) / 10)
                    else:
                        block_count = int((count + 4) / 10) + 1
                        
                    for r in rows:
                        pmt_record = f"{r[0]}{r[1]}{r[2].rjust(8,'0')}{r[3]}{r[4]:<17}{r[5]:010}{r[6]:<15}{r[7]:<22}{r[8]}{r[9]:06}"
                        write_file(file_path,pmt_record)
                        entry_hash += int(r[2])
                        total_credit+= r[5]
                    
                    entry_hash = str(entry_hash)[-10:] #entry has = last 10 digits of the sum of all routing numbers
                    batch_control = f"8220{count:06}{str(entry_hash).ljust(10,'0')}000000000000{total_credit:012}0000000000"\
                                    "                         "\
                                    "056250030000001"
                    write_file(file_path,batch_control)
                    file_control = f"9000001{block_count:06}{count:08}{str(entry_hash).ljust(10,'0')}000000000000{total_credit:012}"
                    write_file(file_path,file_control)
                    end_of_file = "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999"
                    write_file(file_path,end_of_file)
	
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
        
        sql.close()
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