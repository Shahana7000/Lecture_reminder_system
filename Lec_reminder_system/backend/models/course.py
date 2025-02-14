from config import mysql

def create_courses_table():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            course_name VARCHAR(255) NOT NULL UNIQUE
        )
    """)
    mysql.connection.commit()
    cursor.close()
