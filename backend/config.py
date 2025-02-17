from flask import Flask
from flask_mysqldb import MySQL
import os
from twilio.rest import Client

app = Flask(__name__)  # Initialize Flask App

# MySQL Configuration
app.config['MYSQL_HOST'] = '127.0.0.1'  # or 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'okay'
app.config['MYSQL_DB'] = 'lecture_reminder'

mysql = MySQL(app)  # Initialize MySQL Connection

# Twilio Configuration
TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

print("Database connected successfully!")  # Debugging
