from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from config import db, app  # Import database and app configuration

auth = Blueprint('auth', __name__)

# Secret key for JWT
app.config['SECRET_KEY'] = 'your_secret_key'

# Middleware for token verification
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = get_user_by_id(data['id'])
        except:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Function to get user from database
def get_user_by_id(user_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user

# User registration route
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'Missing fields!'}), 400

    hashed_password = generate_password_hash(password, method='sha256')

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, hashed_password))
        db.commit()
    except:
        return jsonify({'message': 'User already exists or database error!'}), 400
    finally:
        cursor.close()

    return jsonify({'message': 'User registered successfully!'}), 201

# User login route
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid email or password!'}), 401

    token = jwt.encode({'id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                       app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token})

# Protected route (Example)
@auth.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': 'Access granted!', 'user': current_user})

