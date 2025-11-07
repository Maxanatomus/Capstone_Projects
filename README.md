# Capstone_Projects
My Data Science and Analytics Capstone Projects demonstrate basic awareness of the statistics, machine learning models development, training and testing, as well as the programming skillset covering all main aspects of the data sciance and data analysiss and visualization proejcts alligned with "PACE" (Plan, Analyze, Construct and Execute) methodology, including:

- exporatory data analysis, including feature engineering, statistics,
- machine learning models construction (build, testing, fine-tuning, validataion)
- translating results into the insights for the business audience.

## Mood Recipe Recommender App

A simple web application that recommends recipes based on your current mood.

### Features
- Select from 6 different moods (Happy, Sad, Stressed, Energetic, Relaxed, Excited)
- Get personalized recipe recommendations
- Request a new recipe if you don't like the current one
- Beautiful, modern UI with Tailwind CSS

### Tech Stack
- **Backend**: Python with Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS (Tailwind), JavaScript

### Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

### Project Structure
```
/workspace/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── recipes.db            # SQLite database (created automatically)
└── static/
    ├── index.html        # Main HTML page
    └── app.js           # Frontend JavaScript
```

### How It Works
1. The app initializes a SQLite database with sample recipes on first run
2. Users select their mood from the available options
3. The backend randomly selects a recipe matching that mood
4. Users can request another recipe for the same mood
5. Users can go back to select a different mood

Enjoy your mood-based recipe recommendations! 🍽️
