import json
from flask import Flask, request, jsonify, render_template, send_from_directory, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import requests
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__,
            static_folder="./static",
            template_folder="./templates")
CORS(app)
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
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for('index'))

@app.route('/protected')
@login_required
def protected():
    return jsonify({'message': f'Hello, {current_user.username}'}), 200

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

