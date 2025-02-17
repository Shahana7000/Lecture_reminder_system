from config import mysql

def create_timetable_table():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timetables (
            id INT AUTO_INCREMENT PRIMARY KEY,
            course_id INT NOT NULL,
            faculty_id INT NOT NULL,
            classroom VARCHAR(50) NOT NULL,
            day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
            lecture_time TIME NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
            FOREIGN KEY (faculty_id) REFERENCES faculties(id) ON DELETE CASCADE
        )
    """)
    mysql.connection.commit()
    cursor.close()
