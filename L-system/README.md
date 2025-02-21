# Lecture Reminder System

## Features
- User authentication (Admin, Faculty)
- Lecture scheduling and management
- Automated reminder notifications
- System statistics and reporting
- Role-based access control

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate environment: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Initialize database: `flask db init && flask db migrate && flask db upgrade`
5. Run application: `flask run`

## Usage
- Access the application at http://localhost:5000
- Use the following test accounts:
  - Admin: admin@example.com / admin123
  - Faculty: faculty@example.com / faculty123
