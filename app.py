from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import database
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize database on startup
database.init_db()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/recipe/<mood>')
def get_recipe(mood):
    """Get a random recipe for the specified mood"""
    valid_moods = ['happy', 'sad', 'stressed', 'energetic', 'relaxed']
    
    if mood.lower() not in valid_moods:
        return jsonify({'error': 'Invalid mood. Choose from: happy, sad, stressed, energetic, relaxed'}), 400
    
    recipe = database.get_recipe_by_mood(mood.lower())
    
    if recipe:
        return jsonify(recipe)
    else:
        return jsonify({'error': 'No recipe found for this mood'}), 404

@app.route('/api/moods')
def get_moods():
    """Get list of available moods"""
    moods = [
        {'value': 'happy', 'label': '😊 Happy', 'emoji': '😊'},
        {'value': 'sad', 'label': '😢 Sad', 'emoji': '😢'},
        {'value': 'stressed', 'label': '😰 Stressed', 'emoji': '😰'},
        {'value': 'energetic', 'label': '⚡ Energetic', 'emoji': '⚡'},
        {'value': 'relaxed', 'label': '😌 Relaxed', 'emoji': '😌'}
    ]
    return jsonify(moods)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
