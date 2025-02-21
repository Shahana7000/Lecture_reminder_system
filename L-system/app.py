from flask import Flask
from config import Config
from flask_migrate import Migrate
from extensions import db, login

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login.init_app(app)
login.login_view = 'auth.login'
migrate = Migrate(app, db)

def register_blueprints():
    from routes import auth_routes, dashboard_routes, lecture_routes, notification_routes
    app.register_blueprint(auth_routes)
    app.register_blueprint(dashboard_routes)
    app.register_blueprint(lecture_routes)
    app.register_blueprint(notification_routes)


def init_scheduler(app):
    from tasks.scheduler import init_scheduler
    init_scheduler(app)


# Register blueprints and initialize scheduler
register_blueprints()
init_scheduler(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
