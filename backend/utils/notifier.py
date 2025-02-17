import schedule
import time
from datetime import datetime
from config import mysql, twilio_client, TWILIO_PHONE_NUMBER

def get_upcoming_lectures():
    """Fetch faculty lectures happening within the next 10 minutes."""
    cursor = mysql.connection.cursor()
    now = datetime.now().strftime("%H:%M")
    
    cursor.execute("""
        SELECT f.id, f.name, f.phone, c.course_name, t.classroom, t.lecture_time 
        FROM timetables t
        JOIN faculties f ON t.faculty_id = f.id
        JOIN courses c ON t.course_id = c.id
        WHERE t.lecture_time = %s
    """, (now,))
    
    lectures = cursor.fetchall()
    cursor.close()
    
    return lectures

def send_sms(phone_number, message):
    """Send SMS using Twilio."""
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )

def send_whatsapp(phone_number, message):
    """Send WhatsApp message using Twilio."""
    twilio_client.messages.create(
        body=message,
        from_="whatsapp:" + TWILIO_PHONE_NUMBER,
        to="whatsapp:" + phone_number
    )

def call_faculty(phone_number):
    """Make an automated call using Twilio."""
    twilio_client.calls.create(
        twiml='<Response><Say>This is a reminder for your upcoming lecture.</Say></Response>',
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )

def check_and_notify():
    """Main function to check timetable and send notifications."""
    lectures = get_upcoming_lectures()

    for lecture in lectures:
        faculty_name = lecture[1]
        phone = lecture[2]
        course = lecture[3]
        classroom = lecture[4]
        time = lecture[5]

        message = f"Reminder: {faculty_name}, you have a {course} lecture at {time} in {classroom}."

        # Send SMS
        send_sms(phone, message)

        # Send WhatsApp
        send_whatsapp(phone, message)

        # Make a Call
        call_faculty(phone)

# Schedule this function to run every minute
schedule.every(1).minutes.do(check_and_notify)

if __name__ == "__main__":
    print("📢 Notification system started...")
    while True:
        schedule.run_pending()
        time.sleep(60)
