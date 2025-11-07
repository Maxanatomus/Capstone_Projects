# 🍳 Mood Recipe Recommender

A simple and beautiful web application that recommends recipes based on your current mood!

## Features

- 🎭 Select from 5 different moods: Happy, Sad, Stressed, Energetic, or Relaxed
- 🍽️ Get personalized recipe recommendations based on your mood
- 🔄 Request new recipes if you don't like the current suggestion
- 📱 Responsive design with beautiful Tailwind CSS styling
- 💾 SQLite database with 15+ pre-loaded recipes

## Tech Stack

**Backend:**
- Python 3
- Flask (web framework)
- SQLite (database)

**Frontend:**
- HTML5
- JavaScript (vanilla)
- Tailwind CSS

## Installation & Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   
   Option A - Using the startup script:
   ```bash
   ./start_app.sh
   ```
   
   Option B - Running directly:
   ```bash
   python3 app.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5000`

## How to Use

1. **Select Your Mood**: Click on one of the five mood buttons that best represents how you're feeling
2. **View Recipe**: The app will display a recipe recommendation tailored to your mood
3. **Try Another**: Don't like the recipe? Click "Try Another Recipe" to get a different suggestion for the same mood
4. **Change Mood**: Click "Change Mood" to go back and select a different mood

## Project Structure

```
.
├── app.py                 # Flask backend server
├── database.py            # Database initialization and queries
├── recipes.db            # SQLite database (auto-created)
├── requirements.txt      # Python dependencies
├── static/
│   ├── index.html       # Main HTML page
│   └── script.js        # Frontend JavaScript
└── RECIPE_APP_README.md  # This file
```

## API Endpoints

- `GET /` - Serves the main HTML page
- `GET /api/moods` - Returns list of available moods
- `GET /api/recipe/<mood>` - Returns a random recipe for the specified mood

## Mood Categories

- **Happy** 😊 - Bright, colorful, and fresh recipes
- **Sad** 😢 - Comfort food to lift your spirits
- **Stressed** 😰 - Quick and easy recipes (15 minutes or less!)
- **Energetic** ⚡ - High-energy, protein-packed meals
- **Relaxed** 😌 - Light, fresh, and calming dishes

## Database

The app uses SQLite to store recipes. The database is automatically initialized with 15+ recipes when you first run the application. Each recipe includes:
- Name
- Mood category
- Ingredients list
- Step-by-step instructions
- Prep time
- Difficulty level

## Customization

### Adding More Recipes

Edit the `database.py` file and add more recipes to the `recipes` list in the `init_db()` function. Each recipe should follow this format:

```python
{
    'name': 'Recipe Name',
    'mood': 'happy',  # or sad, stressed, energetic, relaxed
    'ingredients': json.dumps(['ingredient 1', 'ingredient 2']),
    'instructions': 'Step by step instructions...',
    'prep_time': '30 minutes',
    'difficulty': 'Easy'  # or Medium, Hard
}
```

After adding recipes, delete the `recipes.db` file and restart the server to reinitialize the database.

## Browser Compatibility

Works on all modern browsers:
- Chrome
- Firefox
- Safari
- Edge

## License

This is a simple project created for educational purposes. Feel free to use and modify as needed!

## Future Enhancements

Some ideas for extending this app:
- User authentication
- Save favorite recipes
- Add ratings and reviews
- Search functionality
- Dietary restriction filters (vegetarian, vegan, gluten-free, etc.)
- Meal planning feature
- Shopping list generator

Enjoy cooking based on your mood! 🎉
