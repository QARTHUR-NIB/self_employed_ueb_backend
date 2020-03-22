import cx_Oracle
import os
from flask import Flask, request, jsonify
from modules.application import app
from config import oraDB

