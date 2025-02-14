from flask import Flask
from config import app
from routes.faculty import faculty_blueprint
from routes.timetable import timetable_blueprint

# Register Blueprints (API Routes)
app.register_blueprint(faculty_blueprint, url_prefix="/faculty")
app.register_blueprint(timetable_blueprint, url_prefix="/timetable")

if __name__ == "__main__":
    app.run(debug=True)
