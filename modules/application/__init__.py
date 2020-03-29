from flask import Flask, request, jsonify
from flask_cors import CORS,cross_origin
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from config import jwt
from modules.application.background_jobs.notify_applicants_of_payments import send_notice_to_all_paid_applicants
from apscheduler.schedulers.background import BackgroundScheduler

# initialize scheduler
sched = BackgroundScheduler(daemon=True)
sched.add_job(send_notice_to_all_paid_applicants,'cron',id="payment_notice",hour='17',minute='9',start_date='2020-03-29')
sched.start()

app = Flask(__name__, template_folder="templates")
CORS(app)

UPLOAD_FOLDER = 'C:\\Uploads'
EFT_FILES_FOLDER = 'C:\\Check_Run\\EFT'
MANUAL_CHECK_FOLDER = 'C:\\Check_Run\\Manual Check'
SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\\scripts"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SCRIPT_FOLDER'] = SCRIPT_FOLDER
app.config['EFT_FILES_FOLDER'] = EFT_FILES_FOLDER
app.config['MANUAL_CHECK_FOLDER'] = MANUAL_CHECK_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['JSON_AS_ASCII'] = False
app.config['JWT_SECRET_KEY'] = jwt.secret
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

from .controllers import *
