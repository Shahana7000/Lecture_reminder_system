from flask import Blueprint, request, jsonify
from config import mysql

timetable_blueprint = Blueprint('timetable', __name__)

# 📌 Assign a lecture to a faculty
@timetable_blueprint.route('/assign', methods=['POST'])
def assign_lecture():
    data = request.json
    course_id = data.get('course_id')
    faculty_id = data.get('faculty_id')
    classroom = data.get('classroom')
    day = data.get('day')
    lecture_time = data.get('lecture_time')

    if not all([course_id, faculty_id, classroom, day, lecture_time]):
        return jsonify({'error': 'All fields are required'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO timetables (course_id, faculty_id, classroom, day, lecture_time) 
        VALUES (%s, %s, %s, %s, %s)
    """, (course_id, faculty_id, classroom, day, lecture_time))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Lecture assigned successfully'}), 201

# 📌 Fetch schedule for a specific faculty
@timetable_blueprint.route('/schedule/<int:faculty_id>', methods=['GET'])
def faculty_schedule(faculty_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT courses.course_name, timetables.classroom, timetables.day, timetables.lecture_time
        FROM timetables
        JOIN courses ON timetables.course_id = courses.id
        WHERE timetables.faculty_id = %s
    """, (faculty_id,))
    schedule = cursor.fetchall()
    cursor.close()

    return jsonify(schedule), 200
