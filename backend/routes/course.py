from flask import Blueprint, request, jsonify
from config import mysql

course_blueprint = Blueprint('course', __name__)

# 📌 Add a new course
@course_blueprint.route('/add', methods=['POST'])
def add_course():
    data = request.json
    course_name = data.get('course_name')

    if not course_name:
        return jsonify({'error': 'Course name is required'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO courses (course_name) VALUES (%s)", (course_name,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Course added successfully'}), 201

# 📌 Fetch all courses
@course_blueprint.route('/list', methods=['GET'])
def list_courses():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.close()

    return jsonify(courses), 200
