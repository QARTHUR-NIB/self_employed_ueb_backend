import cx_Oracle
import os
from flask import Flask, request, jsonify
from modules.application import app
from config import oraDB

@app.route('/payments')
def get_payments():
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\Compliance Scripts\Data Migration\Get_Payments.sql"
        sql = open(path,"r")
        params = {"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        result = {"pmt_id":r[0],"employer_nib":r[1],"pmt_type":r[2],
                                "check_num":r[3],"pmt_amt":r[4],"pmt_date":r[5],
                                "pmt_location":r[6],"receipt_num":r[7],"ins_by":r[8],
                                "ins_date":r[9]}
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",data=data,message=f"System Error: {str(e)}"),500


@app.route('/employer/<string:erni>/payments')
def get_employer_payments(erni):
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\Compliance Scripts\Data Migration\Get_Employer_Payments.sql"
        sql = open(path,"r")
        params = {"employer":erni,"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        result = {"pmt_id":r[0],"employer_nib":r[1],"pmt_type":r[2],
                                "check_num":r[3],"pmt_amt":r[4],"pmt_date":r[5],
                                "pmt_location":r[6],"receipt_num":r[7],"ins_by":r[8],
                                "ins_date":r[9]}
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",data=data,message=f"System Error: {str(e)}"),500

@app.route('/employer/<string:erni>/payments/<string:pmt_id>')
def get_employer_payment(erni,pmt_id):
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\Compliance Scripts\Data Migration\Get_Employer_Individual_Payments.sql"
        sql = open(path,"r")
        params = {"employer":erni,"pmt_id":pmt_id,"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        result = {"pmt_id":r[0],"employer_nib":r[1],"pmt_type":r[2],
                                "check_num":r[3],"pmt_amt":r[4],"pmt_date":r[5],
                                "pmt_location":r[6],"receipt_num":r[7],"ins_by":r[8],
                                "ins_date":r[9]}
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",data=data,message=f"System Error: {str(e)}"),500

@app.route('/employer/installment/payments')
def get_all_employer_agreement_payments():
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\Compliance Scripts\Data Migration\Get_IAG_Payments.sql"
        sql = open(path,"r")
        params = {"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        result = {"employer_nib":r[0],"iag_num":r[1],"pmt_type":r[2],
                                "pmt_amt":r[3],"pmt_id":r[4],"add_rev_flag":r[5],
                                "write_off_flag":r[6],"id":r[7]}
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",data=data,message=f"System Error: {str(e)}"),500

@app.route('/employer/<string:erni>/installment/payments/<string:pmt_id>')
def get_iag_payment_details(erni,pmt_id):
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\Compliance Scripts\Data Migration\Get_Installment_Payment(details).sql"
        sql = open(path,"r")
        params = {"employer":erni,"pmt_id":pmt_id,"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        result = {"employer_nib":r[0],"iag_num":r[1],"pmt_type":r[2],
                                "pmt_amt":r[3],"pmt_id":r[4],"add_rev_flag":r[5],
                                "write_off_flag":r[6],"id":r[7]}
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",data=data,message=f"System Error: {str(e)}"),500


@app.route('/employer/<string:erni>/installment/payments')
def get_emp_iag_payment_details(erni):
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\Compliance Scripts\Data Migration\Get_Installment_Payment(employer).sql"
        sql = open(path,"r")
        params = {"employer":erni,"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        result = {"employer_nib":r[0],"iag_num":r[1],"pmt_type":r[2],
                                "pmt_amt":r[3],"pmt_id":r[4],"add_rev_flag":r[5],
                                "write_off_flag":r[6],"id":r[7],"num_records":r[8]}
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",data=data,message=f"System Error: {str(e)}"),500


@app.route('/employer/contribution/payments')
def get_employer_contribution_payments():
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\Compliance Scripts\Data Migration\Get_Contribution_Payments.sql"
        sql = open(path,"r")
        params = {"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        result = {"employer_nib":r[0],"conym":r[1],"pmt_amount":r[2],
                                    "report_id":r[3],"pmt_id":r[4],"add_rev_flag":r[5],
                                    "id":r[6]}
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",message=f"System Error: {str(e)}"),500

@app.route('/employer/<string:erni>/contribution/payments/<string:pmt_id>')
def get_c10_payment_details(erni,pmt_id):
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\Compliance Scripts\Data Migration\Get_Contribution_Payment(details).sql"
        sql = open(path,"r")
        params = {"employer":erni,"pmt_id":pmt_id,"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        result = {"employer_nib":r[0],"conym":r[1],"pmt_amount":r[2],
                                    "report_id":r[3],"pmt_id":r[4],"add_rev_flag":r[5],
                                    "id":r[6]}
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",data=data,message=f"System Error: {str(e)}"),500


@app.route('/employer/<string:erni>/contribution/payments')
def get_emp_c10_payment_details(erni):
    try:
        data = []
        path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\Compliance Scripts\Data Migration\Get_Contribution_Payment(employer).sql"
        sql = open(path,"r")
        params = {"employer":erni,"page_size":int(request.args['page_size']),"page_number":int(request.args['page_num'])}
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        result = {"employer_nib":r[0],"conym":r[1],"pmt_amount":r[2],
                                    "report_id":r[3],"pmt_id":r[4],"add_rev_flag":r[5],
                                    "id":r[6],"num_records":r[7]}
                        data.append(result)
        sql.close()
        return jsonify(success="Y",data=data),200
    except Exception as e:
        return jsonify(success="N",data=data,message=f"System Error: {str(e)}"),500