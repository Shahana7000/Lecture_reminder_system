from models.course import create_courses_table
from models.faculty import create_faculty_table
from models.timetable import create_timetable_table

def initialize_database():
    create_courses_table()
    create_faculty_table()
    create_timetable_table()
    print("✅ Database Tables Created Successfully!")

initialize_database()
