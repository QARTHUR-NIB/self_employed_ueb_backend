import cx_Oracle
import os
from flask import Flask, request, jsonify
from modules.application import app
from config import oraDB

class ValidationException(Exception):
    pass

@app.route('/person/<string:eeni>',methods = ["POST"])
def get_reg(eeni):
    try:
        ni_num_exists = None
        vaild_first_name = None
        valid_last_name = None
        valid_dob = None
        weekly_pmt_amt_gte_200 = None
        success = None
        path = os.path.join(app.config['SCRIPT_FOLDER'],"validate_reg_nib#.sql")
        #path = r"\\jumvmfileprdcfs\Vitech\SQL Scripts\SelfEmployed_UEB\validate_reg_nib#.sql"
        params = request.json
        params.update([("eeni",eeni)])
        sql = open(path,"r")
        with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
            with conn.cursor() as cursor:
                results = cursor.execute(sql.read(),params)
                while True:
                    rows = results.fetchall()
                    if not rows:
                        break
                    for r in rows:
                        ni_num_exists = r[0]
                        vaild_first_name = r[1]
                        valid_last_name = r[2]
                        valid_dob = r[3]
                        weekly_pmt_amt_gte_200= r[4]

                if ni_num_exists is None or ni_num_exists == 'N':
                    success='N'
                    raise ValidationException("NIB Number does not exist")
                else:
                    success='Y'
                
                if vaild_first_name is None or vaild_first_name == 'N':
                    success='N'
                    raise ValidationException("First name does not match NIB's records")
                else:
                    success='Y'

                if valid_last_name is None or valid_last_name == 'N':
                    success='N'
                    raise ValidationException("Last name does not match NIB's records")
                else:
                    success='Y'
                
                if valid_dob is None or valid_dob == 'N':
                    success='N'
                    raise ValidationException("Date of birth does not match NIB's records")
                else:
                    success='Y'
                
                if weekly_pmt_amt_gte_200 is None or weekly_pmt_amt_gte_200 == 'Y':
                    success='N'
                    raise ValidationException("Your current NIB benefit exceeds $200 per week")
                else:
                    success='Y'

        sql.close()
        return jsonify(success=success,message=""),200
    except ValidationException as e:
        return jsonify(success=success,message=f"{str(e)}"),400
    except Exception as e:
        return jsonify(success=success,message=f"System Error: {str(e)}"),500