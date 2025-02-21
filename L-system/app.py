from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
mail = Mail(app)

# Import models after extensions are initialized
from models import User, Lecture, Notification

# Import routes
from routes import auth_routes, dashboard_routes, lecture_routes, notification_routes

# Register blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(dashboard_routes)
app.register_blueprint(lecture_routes)
app.register_blueprint(notification_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
