from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Lecture, Notification, Timetable
from extensions import db


# Create blueprints
auth_routes = Blueprint('auth', __name__)
dashboard_routes = Blueprint('dashboard', __name__)
lecture_routes = Blueprint('lecture', __name__)
notification_routes = Blueprint('notification', __name__)

# Root route
@auth_routes.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('dashboard.admin_dashboard'))
        else:
            return redirect(url_for('dashboard.faculty_dashboard'))
    return redirect(url_for('auth.login'))

# Authentication routes
@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard.admin_dashboard' if user.role == 'admin' else 'dashboard.faculty_dashboard'))
        flash('Invalid email or password')
    return render_template('login.html')

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))
        
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Dashboard routes
@dashboard_routes.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.faculty_dashboard'))
    
    users = User.query.all()
    lectures = Lecture.query.all()
    notifications = Notification.query.all()
    
    return render_template('admin_dashboard.html', 
                         users=users, 
                         lectures=lectures, 
                         notifications=notifications)

# Admin CRUD operations
@dashboard_routes.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.faculty_dashboard'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!')
    return redirect(url_for('dashboard.admin_dashboard'))

@dashboard_routes.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.faculty_dashboard'))
    
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        if request.form['password']:
            user.set_password(request.form['password'])
        db.session.commit()
        flash('User updated successfully!')
        return redirect(url_for('dashboard.admin_dashboard'))
    
    return render_template('edit_user.html', user=user)


@dashboard_routes.route('/admin/lecture/<int:lecture_id>/delete', methods=['POST'])
@login_required
def delete_lecture(lecture_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.faculty_dashboard'))
    
    lecture = Lecture.query.get_or_404(lecture_id)
    db.session.delete(lecture)
    db.session.commit()
    flash('Lecture deleted successfully!')
    return redirect(url_for('dashboard.admin_dashboard'))

@dashboard_routes.route('/admin/notification/<int:notification_id>/delete', methods=['POST'])
@login_required
def delete_notification(notification_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.faculty_dashboard'))
    
    notification = Notification.query.get_or_404(notification_id)
    db.session.delete(notification)
    db.session.commit()
    flash('Notification deleted successfully!')
    return redirect(url_for('dashboard.admin_dashboard'))

# Timetable Management Routes
@dashboard_routes.route('/admin/timetable')
@login_required
def manage_timetable():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.faculty_dashboard'))
    
    timetable = Timetable.query.order_by(Timetable.start_time.asc()).all()
    return render_template('admin_timetable.html', timetable=timetable)

@dashboard_routes.route('/admin/timetable/new', methods=['GET', 'POST'])
@login_required
def new_timetable_entry():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.faculty_dashboard'))
    
    if request.method == 'POST':
        course_name = request.form['course_name']
        subject = request.form['subject']
        faculty_id = request.form['faculty_id']
        start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')
        
        new_entry = Timetable(
            course_name=course_name,
            subject=subject,
            faculty_id=faculty_id,
            start_time=start_time,
            end_time=end_time
        )
        db.session.add(new_entry)
        db.session.commit()
        flash('Timetable entry created successfully!')
        return redirect(url_for('dashboard.manage_timetable'))
    
    faculties = User.query.filter_by(role='faculty').all()
    return render_template('edit_timetable.html', faculties=faculties)

@dashboard_routes.route('/admin/timetable/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_timetable_entry(entry_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.faculty_dashboard'))
    
    entry = Timetable.query.get_or_404(entry_id)
    if request.method == 'POST':
        entry.course_name = request.form['course_name']
        entry.subject = request.form['subject']
        entry.faculty_id = request.form['faculty_id']
        entry.start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        entry.end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')
        db.session.commit()
        flash('Timetable entry updated successfully!')
        return redirect(url_for('dashboard.manage_timetable'))
    
    faculties = User.query.filter_by(role='faculty').all()
    return render_template('edit_timetable.html', entry=entry, faculties=faculties)

@dashboard_routes.route('/admin/timetable/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete_timetable_entry(entry_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.faculty_dashboard'))
    
    entry = Timetable.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Timetable entry deleted successfully!')
    return redirect(url_for('dashboard.manage_timetable'))

@dashboard_routes.route('/faculty')
@login_required
def faculty_dashboard():
    lectures = Lecture.query.filter_by(lecturer_id=current_user.id).all()
    notifications = Notification.query.filter_by(user_id=current_user.id).all()
    
    return render_template('faculty_dashboard.html', 
                         lectures=lectures, 
                         notifications=notifications)

# Lecture routes
@lecture_routes.route('/lecture/create', methods=['POST'])
@login_required
def create_lecture():
    if request.method == 'POST':
        course_name = request.form['course_name']
        scheduled_time = datetime.strptime(request.form['scheduled_time'], '%Y-%m-%dT%H:%M')
        location = request.form['location']
        
        new_lecture = Lecture(
            course_name=course_name,
            lecturer_id=current_user.id,
            scheduled_time=scheduled_time,
            location=location
        )
        db.session.add(new_lecture)
        db.session.commit()
        flash('Lecture created successfully!')
    return redirect(url_for('dashboard.faculty_dashboard'))

# Notification routes
@notification_routes.route('/notification/send', methods=['POST'])
@login_required
def send_notification():
    if request.method == 'POST':
        lecture_id = request.form['lecture_id']
        message = request.form['message']
        
        lecture = Lecture.query.get(lecture_id)
        if lecture:
            new_notification = Notification(
                user_id=lecture.lecturer_id,
                lecture_id=lecture_id,
                message=message
            )
            db.session.add(new_notification)
            db.session.commit()
            flash('Notification sent successfully!')
    return redirect(url_for('dashboard.faculty_dashboard'))
