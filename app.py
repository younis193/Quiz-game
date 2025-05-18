import os
import json
import logging
from flask import Flask, render_template, request, jsonify, session

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Load questions from JSON file
def load_questions():
    try:
        with open('static/data/questions.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading questions: {e}")
        return {}

# Routes
@app.route('/')
def index():
    """Render the home page with category and difficulty selection"""
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    """Render the quiz page"""
    category = request.args.get('category', 'science')
    difficulty = request.args.get('difficulty', 'easy')
    
    # Store category and difficulty in session
    session['category'] = category
    session['difficulty'] = difficulty
    
    return render_template('quiz.html', category=category, difficulty=difficulty)

@app.route('/get_questions')
def get_questions():
    """API endpoint to get questions based on category and difficulty"""
    category = request.args.get('category', 'science')
    difficulty = request.args.get('difficulty', 'easy')
    
    questions_data = load_questions()
    
    # Filter questions by category and difficulty
    if category in questions_data and difficulty in questions_data[category]:
        return jsonify(questions_data[category][difficulty])
    else:
        return jsonify([])

@app.route('/results')
def results():
    """Render the results page"""
    return render_template('results.html')

@app.route('/leaderboard')
def leaderboard():
    """Render the leaderboard page"""
    return render_template('leaderboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
