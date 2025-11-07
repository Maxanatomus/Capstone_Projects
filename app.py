from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import random
import os

app = Flask(__name__, static_folder='static')
CORS(app)

DATABASE = 'recipes.db'

def init_db():
    """Initialize the database with recipes"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Create recipes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mood TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Check if recipes already exist
    c.execute('SELECT COUNT(*) FROM recipes')
    count = c.fetchone()[0]
    
    if count == 0:
        # Seed with sample recipes
        recipes = [
            # Happy mood recipes
            ("Chocolate Chip Cookies", "happy", "2 cups flour, 1 cup butter, 1 cup sugar, 2 eggs, 1 cup chocolate chips", "Mix ingredients, bake at 375°F for 10 minutes", "Sweet treats to boost your happiness!"),
            ("Rainbow Smoothie Bowl", "happy", "Mixed berries, banana, yogurt, granola, honey", "Blend fruits, top with granola and honey", "Colorful and energizing!"),
            ("Mac and Cheese", "happy", "Pasta, cheese, butter, milk, breadcrumbs", "Cook pasta, make cheese sauce, bake until golden", "Comfort food classic!"),
            
            # Sad mood recipes
            ("Chicken Noodle Soup", "sad", "Chicken, noodles, carrots, celery, onion, broth", "Simmer chicken and vegetables, add noodles, cook until tender", "Warm and comforting soup"),
            ("Warm Chocolate Cake", "sad", "Chocolate, butter, eggs, sugar, flour", "Melt chocolate, mix ingredients, bake at 350°F for 25 minutes", "Rich and comforting dessert"),
            ("Mashed Potatoes", "sad", "Potatoes, butter, milk, salt, pepper", "Boil potatoes, mash with butter and milk, season", "Creamy comfort food"),
            
            # Stressed mood recipes
            ("Green Tea Smoothie", "stressed", "Green tea, banana, spinach, honey, ice", "Brew tea, blend with fruits and ice", "Calming and refreshing"),
            ("Oatmeal with Berries", "stressed", "Oats, milk, berries, honey, nuts", "Cook oats, top with berries and nuts", "Nourishing and calming"),
            ("Herbal Tea", "stressed", "Chamomile tea, honey, lemon", "Steep tea, add honey and lemon", "Soothing herbal blend"),
            
            # Energetic mood recipes
            ("Protein Power Bowl", "energetic", "Quinoa, chicken, vegetables, avocado, tahini", "Cook quinoa, grill chicken, assemble bowl", "High-protein energy boost"),
            ("Energy Smoothie", "energetic", "Banana, spinach, protein powder, almond milk, dates", "Blend all ingredients until smooth", "Quick energy boost"),
            ("Grilled Salmon Salad", "energetic", "Salmon, mixed greens, quinoa, vegetables, lemon", "Grill salmon, assemble salad with quinoa", "Light and energizing"),
            
            # Relaxed mood recipes
            ("Mediterranean Pasta", "relaxed", "Pasta, tomatoes, olives, feta, olive oil, herbs", "Cook pasta, toss with vegetables and feta", "Light and flavorful"),
            ("Yoga Bowl", "relaxed", "Brown rice, chickpeas, vegetables, tahini dressing", "Cook rice, roast vegetables, assemble bowl", "Balanced and nourishing"),
            ("Fruit Salad", "relaxed", "Mixed seasonal fruits, mint, honey", "Chop fruits, drizzle with honey, garnish with mint", "Fresh and light"),
            
            # Excited mood recipes
            ("Spicy Tacos", "excited", "Tortillas, ground beef, spices, cheese, salsa, avocado", "Cook meat with spices, assemble tacos with toppings", "Bold and flavorful!"),
            ("BBQ Chicken Wings", "excited", "Chicken wings, BBQ sauce, spices", "Season wings, bake or grill, toss in BBQ sauce", "Fiery and fun!"),
            ("Loaded Nachos", "excited", "Tortilla chips, cheese, jalapeños, salsa, sour cream", "Layer chips and cheese, bake, top with toppings", "Party favorite!"),
        ]
        
        c.executemany('''
            INSERT INTO recipes (name, mood, ingredients, instructions, description)
            VALUES (?, ?, ?, ?, ?)
        ''', recipes)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/moods', methods=['GET'])
def get_moods():
    """Get list of available moods"""
    moods = ['happy', 'sad', 'stressed', 'energetic', 'relaxed', 'excited']
    return jsonify(moods)

@app.route('/api/recipe', methods=['GET'])
def get_recipe():
    """Get a random recipe for a given mood"""
    mood = request.args.get('mood')
    exclude_id = request.args.get('exclude_id', type=int)
    
    if not mood:
        return jsonify({'error': 'Mood parameter is required'}), 400
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Build query
    query = 'SELECT id, name, mood, ingredients, instructions, description FROM recipes WHERE mood = ?'
    params = [mood]
    
    if exclude_id:
        query += ' AND id != ?'
        params.append(exclude_id)
    
    c.execute(query, params)
    recipes = c.fetchall()
    conn.close()
    
    if not recipes:
        return jsonify({'error': f'No recipes found for mood: {mood}'}), 404
    
    # Select random recipe
    recipe = random.choice(recipes)
    
    return jsonify({
        'id': recipe[0],
        'name': recipe[1],
        'mood': recipe[2],
        'ingredients': recipe[3],
        'instructions': recipe[4],
        'description': recipe[5]
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
