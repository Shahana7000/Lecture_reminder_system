# from flask import Flask
# from flask_mysqldb import MySQL
# import os

# app = Flask(__name__)

# # MySQL Configuration
# app.config['MYSQL_HOST'] = 'localhost'  # Change if using a remote DB
# app.config['MYSQL_USER'] = 'your_username'
# app.config['MYSQL_PASSWORD'] = 'your_password'
# app.config['MYSQL_DB'] = 'lecture_reminder'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# # Initialize MySQL
# mysql = MySQL(app)

from flask_mysqldb import MySQL
import os
from twilio.rest import Client

# MySQL Configuration
mysql = MySQL()

DB_CONFIG = {
    'MYSQL_HOST': 'localhost',
    'MYSQL_USER': 'root',
    'MYSQL_PASSWORD': 'yourpassword',
    'MYSQL_DB': 'lecture_reminder',
}

# Twilio Configuration
TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
