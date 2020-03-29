import cx_Oracle
import os
from modules.application.background_jobs.mailer.Html_Mailer import send_mail
from config import oraDB

def send_notice_to_all_paid_applicants():
    email_events = []
    email_events.append("Payment Generated")
    scripts_folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"scripts")
    with cx_Oracle.connect(f"{oraDB.user_name}/{oraDB.password}@{oraDB.db}") as conn:
        with conn.cursor() as cursor:
            path = os.path.join(scripts_folder_path ,"get_paid_applications_without_payment_notifications.sql")
            sql = open(path,"r")
            results = cursor.execute(sql.read())
            while True:
                rows = results.fetchall()
                if not rows:
                    break

                for r in rows:
                    application = {"first_name":r[0],"beg_pay_period":r[1],"end_pay_period":r[2],
                                    "num_weeks_paid":r[3],"max_weeks":r[4],"pmt_type":r[5],
                                    "branch_name":r[6],"bank_account_number":r[7],"pmt_id":r[8],
                                    "email":r[9]}
                                    
                    send_mail(email_events,application)

                    #update payment info
                    with conn.cursor() as update_cursor:
                        params = {"pmt_id":application["pmt_id"]}
                        script_path = os.path.join(scripts_folder_path,"update_payment_notice.sql")
                        update_sql = open(script_path,"r")
                        update_cursor.execute(update_sql.read(),params)
                        conn.commit()
                        update_sql.close()


