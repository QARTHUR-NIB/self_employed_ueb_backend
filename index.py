import os
import sys
from flask import jsonify, request
from config import flask

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

from modules.application import app

@app.route('/')
def index():
    return jsonify("Hello World"), 200

if __name__ == '__main__':
    app.run(host=flask.host, port=flask.port,debug=True)