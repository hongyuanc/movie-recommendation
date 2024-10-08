import json
from flask import Flask, request, jsonify, render_template, send_from_directory, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import requests
import os
from datetime import datetime, timedelta
import jwt

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__,)

app.config['SECRET_KEY'] = os.environ.get('secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('database_uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
CORS(app)

# Database models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# TMDB API integration
TMDB_ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def get_movie_details(movie_id):
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}", params={'api_key': TMDB_ACCESS_TOKEN})
    return response.json()

def get_new_movies():
    headers = {
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    response = requests.get(f"{TMDB_BASE_URL}/movie/now_playing", headers=headers)
    return response.json()

def generate_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


# Routes
@app.route('/api/movies/new', methods=['GET'])
def new_movies():
    movies_data = get_new_movies()
    return jsonify(movies_data)

@app.route('/api/movies/recommend', methods=['GET'])
def recommend_movies():
    # dummy response
    return jsonify({'recommendations': ['Movie 1', 'Movie 2', 'Movie 3']})

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message')
    # dummy response
    return jsonify({'response': f"You said: {user_message}"})

@app.route('/api/user/dashboard', methods=['GET'])
def user_dashboard():
    return jsonify({
        'user': 'current_user.username',
        'watched_movies': 15,
        'favorite_genre': 'Sci-Fi'
    })

@app.route('/')
def index():
    movies_data = get_new_movies()
    movies = []
    for movie in movies_data['results'][:12]:  # Limit to 12 movies for this example
        movies.append({
            'title': movie['title'],
            'release_date': movie['release_date'],
            'vote_average': movie['vote_average'],
            'poster_path': movie['poster_path']
        })
    return render_template('index.html', movies=movies)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = generate_token(user.id)
        return jsonify({'token': token, 'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/protected')
@login_required
def protected():
    return jsonify({'message': f'Hello, {current_user.username}'}), 200

if __name__ == '__main__':
    app.run(debug=True)

