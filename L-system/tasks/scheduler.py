from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import current_app
from models import Timetable, User
from utils.sms import send_sms

scheduler = BackgroundScheduler()

def check_upcoming_lectures(app):
    with app.app_context():
        reminder_minutes = app.config['SMS_REMINDER_MINUTES']
        now = datetime.utcnow()
        reminder_time = now + timedelta(minutes=reminder_minutes)

        
        # Get lectures starting within the reminder window
        upcoming_lectures = Timetable.query.filter(
            Timetable.start_time.between(now, reminder_time)
        ).all()
        
        for lecture in upcoming_lectures:
            faculty = User.query.get(lecture.faculty_id)
            if faculty and faculty.phone_number:
                message = f"Reminder: {lecture.subject} lecture starts at {lecture.start_time.strftime('%H:%M')}"
                send_sms(faculty.phone_number, message)

def init_scheduler(app):
    scheduler.add_job(
        func=check_upcoming_lectures,
        args=[app],
        trigger='interval',
        minutes=1,
        id='lecture_reminder',
        replace_existing=True
    )
    scheduler.start()
