from flask import Blueprint, request, jsonify
from config import mysql

faculty_blueprint = Blueprint('faculty', __name__)

# 📌 Add a faculty member
@faculty_blueprint.route('/add', methods=['POST'])
def add_faculty():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')

    if not name or not phone:
        return jsonify({'error': 'Name and phone are required'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO faculties (name, phone) VALUES (%s, %s)", (name, phone))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Faculty added successfully'}), 201

# 📌 Fetch all faculty members
@faculty_blueprint.route('/list', methods=['GET'])
def list_faculty():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM faculties")
    faculty = cursor.fetchall()
    cursor.close()

    return jsonify(faculty), 200
