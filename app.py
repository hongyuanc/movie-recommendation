import json
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import requests
import os

app = Flask(__name__,
            static_folder="./static",
            template_folder="./templates")
CORS(app)
app.config['SECRET_KEY'] = os.getenv('secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
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
TMDB_API_KEY = 'your_tmdb_api_key_here'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def get_movie_details(movie_id):
    response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}", params={'api_key': TMDB_API_KEY})
    return response.json()

# Routes
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
    # dummy response
    return jsonify({
        'user': 'John Doe',
        'watched_movies': 15,
        'favorite_genre': 'Sci-Fi'
    })

@app.route('/')
def serve_vue_app():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200

@app.route('/protected')
@login_required
def protected():
    return jsonify({'message': f'Hello, {current_user.username}'}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

