import cx_Oracle
from flask import Flask, request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from modules.application import app
from config import oraDB
import os
from datetime import datetime
from modules.application.background_jobs.mailer.Html_Mailer import send_mail
import csv
import logging
from modules.application.repositories.LumpSumCheckRun import LumpSumCheckRun

LOG_FOLDER = 'C:\\Check_Run\\Logs'
logging.basicConfig(filename=os.path.join(LOG_FOLDER,f"check_run_{datetime.today().strftime('%Y-%m-%d')}.log"),filemode='a',
                    level=logging.INFO,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger()

def write_eft_file(file_path,line):
    with open(file_path,'a') as eft:
        log.info(f"Writing:{file_path} : {line}")
        eft.write(line)
        eft.write("\n")

def write_CSV_file(file_path,row):
    with open(file_path,'a',newline='') as csv_file:
        log.info(f"Writing:{file_path} : {row}")
        writer = csv.writer(csv_file,delimiter=",",quotechar='"',quoting=csv.QUOTE_MINIMAL)
        writer.writerow(tuple(row))

def execute_check_run(user_name):
    try:
        log.info("Initiating Check Run") 
        #Execute Check Run DB Process (Generate Payments in Pending Status)
        checkrun = LumpSumCheckRun()
        checkrun.generateLumpSumPayments()
        # conn = cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}")
        # cursor = conn.cursor()
        # success = cursor.var(cx_Oracle.STRING,1) if not None else ''
        # message = cursor.var(cx_Oracle.STRING,250) if not None else ''
        # cursor.callproc("client.create_se_ueb_checks",[user_name,success,message])

        # if success.getvalue() == "N":
        #     raise Exception(f"Error Generating Payments: {message.getvalue()}")

        log.info("Pending Payments Generated")
        data = []
        email_events = []
        scripts_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"scripts")
        file_header = None
        batch_header = None
        count = 0
        block_count = 0
        entry_hash = 0
        total_credit = 0
        EFT_FILES_FOLDER = 'C:\\Check_Run\\EFT'
        MANUAL_CHECK_FOLDER = 'C:\\Check_Run\\Manual Check'
        SUN_CASH_FOLDER = 'C:\\Check_Run\\Sun Cash'
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                
                log.info("Executing Proc to create batch payment history")
                #write payments for check run to batch payment history
                success = cursor.var(cx_Oracle.STRING,1) if not None else ''
                message = cursor.var(cx_Oracle.STRING,250) if not None else ''
                cursor.callproc("client.create_batch_pmt_history",[user_name,success,message])

                if success.getvalue() == "N":
                    raise Exception(f"Error Writing Payment Batch History: {message.getvalue()}")

                log.info("Batch Payment History Created")
                log.info("Generating EFT payment file")
                #process EFT Files
                path = os.path.join(scripts_path,"get_eft_pending_payments.sql")
                sql = open(path,"r")
                results = cursor.execute(sql.read())
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    #Write EFT File(Nacha File Format)    
                    file_name = f"SE_UEB_EFT_{datetime.today().strftime('%Y-%m-%d-%I%M')}.txt"
                    file_path = os.path.join(EFT_FILES_FOLDER,file_name)
                    file_header = f"101 0056250030000000000{datetime.today().strftime('%y%m%d')}{datetime.today().strftime('%I%M')}1094101Royal Bank of Canada"\
                                    "   National Insurance             "
                    write_eft_file(file_path,file_header)
                    batch_header = f"5220NIB             Long Term Benefits  0002197192PPDClaims    {datetime.today().strftime('%y%m%d')}{datetime.today().strftime('%y%m%d')}"\
                                    "0001056250030000001"
                    write_eft_file(file_path,batch_header)
                    count =  len(rows)
                    if (count + 4) % 10 == 0:
                        block_count = int((count + 4) / 10)
                    else:
                        block_count = int((count + 4) / 10) + 1
                        
                    for r in rows:
                        pmt_record = f"{r[0]}{r[1]}{r[2].rjust(8,'0')}{r[3]}{r[4]:<17}{r[5]:010}{r[6]:<15}{r[7]:<22}{r[8]}{r[9]:06}"
                        write_eft_file(file_path,pmt_record)
                        entry_hash += int(r[2])
                        total_credit+= r[5]
                    
                    entry_hash = str(entry_hash)[-10:] #entry has = last 10 digits of the sum of all routing numbers
                    batch_control = f"8220{count:06}{entry_hash:0>10}000000000000{total_credit:012}0000000000"\
                                    "                         "\
                                    "056250030000001"
                    write_eft_file(file_path,batch_control)
                    file_control = f"9000001{block_count:06}{count:08}{entry_hash:0>10}000000000000{total_credit:012}"
                    write_eft_file(file_path,file_control)
                    end_of_file = "9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999"
                    write_eft_file(file_path,end_of_file)
                    sql.close()

                log.info(f"EFT Payment File Written Successfully")
                log.info(f"Generating Manual Check File")
                #Write Manual Check Payments
                file_name = f"SE_UEB_MANUAL_{datetime.today().strftime('%Y-%m-%d-%I%M')}.csv"
                file_path = os.path.join(MANUAL_CHECK_FOLDER,file_name)
                path = os.path.join(scripts_path,"get_pending_reissued_manual_payments.sql")
                sql = open(path,"r") 
                results = cursor.execute(sql.read())
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        write_CSV_file(file_path,r)
                    sql.close()

                log.info(f"Manual Check File Written Successfully")
                log.info(f"Generating Sun Cash Payment File")
                #Write Sun Cash Payments
                file_name = f"SE_UEB_SUN_CASH_{datetime.today().strftime('%Y-%m-%d-%I%M')}.csv"
                file_path = os.path.join(SUN_CASH_FOLDER,file_name)
                path = os.path.join(scripts_path,"get_pending_reissued_sun_cash_payments.sql")
                sql = open(path,"r") 
                results = cursor.execute(sql.read())
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        write_CSV_file(file_path,r)
                    sql.close()
                
                log.info(f"Sun Cash Payment File Written Successfully")
                log.info(f"Updating all Pending/Reissued Payments to Paid")
                #update all pending payments to paid
                script_path = os.path.join(scripts_path,"mark_pending_reissued_pmts_paid.sql")
                update_sql = open(script_path,"r") 
                cursor.execute(update_sql.read())
                conn.commit()
                update_sql.close()
                #notify users
                log.info(f"All Pending/Reissued Payments marked as Paid")
                log.info(f"Sending Successful Email...")
                email_events.append("Check Run Completed")
                send_mail(email_events,None)
                log.info(f"Check Run Success Email Sent")
    except Exception as e:
        error_message = str(e)
        log.error(f"Check Run Aborted: {error_message}")
        email_events = []
        email_events.append("Check Run Aborted")
        send_mail(email_events,error_message)
