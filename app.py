from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
import os

app = Flask(__name__,
            static_folder="./static",
            template_folder="./templates")
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

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

if __name__ == '__main__':
    app.run(debug=True)