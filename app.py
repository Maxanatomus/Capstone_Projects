import os
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request


DB_PATH = Path(__file__).with_name("recipes.db")

SEED_RECIPES = [
    {
        "mood": "happy",
        "title": "Sunshine Mango Salsa Tacos",
        "ingredients": [
            "8 small corn tortillas",
            "2 ripe mangos, diced",
            "1 red bell pepper, diced",
            "1 avocado, sliced",
            "1/2 cup red onion, finely chopped",
            "1/4 cup fresh cilantro, chopped",
            "Juice of 1 lime",
            "1/2 tsp chili powder",
            "Salt and pepper to taste",
        ],
        "instructions": [
            "Warm the corn tortillas in a dry skillet over medium heat for 1 minute per side.",
            "Combine mango, bell pepper, red onion, cilantro, lime juice, chili powder, salt, and pepper in a bowl to make the salsa.",
            "Fill each tortilla with avocado slices and spoonfuls of mango salsa.",
            "Serve immediately with extra lime wedges on the side.",
        ],
    },
    {
        "mood": "happy",
        "title": "Bubbly Berry Sparkler",
        "ingredients": [
            "1 cup sparkling water",
            "1/2 cup mixed berries (fresh or frozen)",
            "1 tbsp honey",
            "Juice of 1/2 lemon",
            "Fresh mint leaves for garnish",
        ],
        "instructions": [
            "In a glass, muddle the berries with honey and lemon juice.",
            "Add ice and pour sparkling water over the mixture.",
            "Stir gently and garnish with mint leaves.",
            "Serve chilled.",
        ],
    },
    {
        "mood": "relaxed",
        "title": "Creamy Mushroom Risotto",
        "ingredients": [
            "1 cup Arborio rice",
            "4 cups vegetable broth, warmed",
            "1 tbsp olive oil",
            "1 tbsp butter",
            "1 small onion, finely chopped",
            "2 cloves garlic, minced",
            "2 cups sliced mushrooms",
            "1/2 cup grated Parmesan cheese",
            "Salt and pepper to taste",
        ],
        "instructions": [
            "Heat olive oil and butter in a saucepan over medium heat. Sauté onion and garlic until translucent.",
            "Add mushrooms and cook until softened.",
            "Stir in Arborio rice and cook for 1 minute until lightly toasted.",
            "Add warm broth one ladle at a time, stirring until absorbed before adding more, until rice is creamy.",
            "Stir in Parmesan cheese, season with salt and pepper, and serve warm.",
        ],
    },
    {
        "mood": "relaxed",
        "title": "Chamomile Honey Latte",
        "ingredients": [
            "1 cup milk (dairy or plant-based)",
            "1 chamomile tea bag",
            "1 tsp honey",
            "1/4 tsp vanilla extract",
            "Ground cinnamon for garnish",
        ],
        "instructions": [
            "Warm the milk in a small saucepan until steaming but not boiling.",
            "Remove from heat, add the chamomile tea bag, and steep for 5 minutes.",
            "Discard the tea bag and stir in honey and vanilla.",
            "Froth the milk if desired, pour into a mug, and sprinkle with cinnamon.",
        ],
    },
    {
        "mood": "stressed",
        "title": "Comforting Lentil Soup",
        "ingredients": [
            "1 tbsp olive oil",
            "1 onion, diced",
            "2 carrots, diced",
            "2 celery stalks, diced",
            "2 cloves garlic, minced",
            "1 cup dried lentils, rinsed",
            "4 cups vegetable broth",
            "1 tsp dried thyme",
            "1 bay leaf",
            "Salt and pepper to taste",
        ],
        "instructions": [
            "Heat olive oil in a large pot over medium heat. Sauté onion, carrots, and celery until softened.",
            "Add garlic and cook for 1 minute until fragrant.",
            "Add lentils, broth, thyme, and bay leaf. Bring to a boil, then reduce heat and simmer for 25-30 minutes until lentils are tender.",
            "Remove bay leaf, season with salt and pepper, and serve warm.",
        ],
    },
    {
        "mood": "stressed",
        "title": "Dark Chocolate Banana Bites",
        "ingredients": [
            "2 ripe bananas",
            "1/2 cup dark chocolate chips",
            "1 tsp coconut oil",
            "Crushed nuts or shredded coconut for topping (optional)",
        ],
        "instructions": [
            "Slice bananas into rounds and place on a parchment-lined tray.",
            "Melt chocolate chips with coconut oil in the microwave in 20-second intervals, stirring between each.",
            "Dip each banana slice in chocolate and return to the tray.",
            "Sprinkle with toppings if desired and freeze for 30 minutes before serving.",
        ],
    },
    {
        "mood": "adventurous",
        "title": "Spicy Kimchi Fried Rice",
        "ingredients": [
            "2 cups cooked rice (preferably day-old)",
            "1 cup chopped kimchi",
            "1 tbsp gochujang (Korean chili paste)",
            "2 green onions, sliced",
            "1 tbsp sesame oil",
            "1 tbsp soy sauce",
            "2 eggs",
            "Sesame seeds for garnish",
        ],
        "instructions": [
            "Heat sesame oil in a skillet over medium-high heat.",
            "Add kimchi and cook for 2 minutes until fragrant.",
            "Stir in rice, gochujang, and soy sauce, cooking until rice is heated through.",
            "Push rice to one side of the pan, scramble the eggs on the other side, then mix together.",
            "Serve hot, topped with green onions and sesame seeds.",
        ],
    },
    {
        "mood": "adventurous",
        "title": "Matcha Coconut Chia Pudding",
        "ingredients": [
            "1 can (13.5 oz) coconut milk",
            "3 tbsp chia seeds",
            "1 tsp matcha powder",
            "1 tbsp maple syrup",
            "Fresh fruit for topping",
        ],
        "instructions": [
            "Whisk coconut milk, matcha powder, and maple syrup until smooth.",
            "Stir in chia seeds and refrigerate for at least 3 hours or overnight.",
            "Stir again before serving and top with fresh fruit.",
        ],
    },
]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT NOT NULL,
            title TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL
        );
        """
    )

    cursor.execute("SELECT COUNT(*) FROM recipes")
    (count,) = cursor.fetchone()

    if count == 0:
        for recipe in SEED_RECIPES:
            cursor.execute(
                """
                INSERT INTO recipes (mood, title, ingredients, instructions)
                VALUES (?, ?, ?, ?)
                """,
                (
                    recipe["mood"],
                    recipe["title"],
                    "\n".join(recipe["ingredients"]),
                    "\n".join(recipe["instructions"]),
                ),
            )

    conn.commit()
    conn.close()


app = Flask(__name__)
init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/moods")
def list_moods():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT mood FROM recipes ORDER BY mood ASC")
    moods = [row["mood"] for row in cursor.fetchall()]
    conn.close()
    return jsonify({"moods": moods})


@app.route("/api/recipe")
def get_recipe():
    mood = request.args.get("mood")
    if not mood:
        return jsonify({"error": "Mood query parameter is required."}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT mood, title, ingredients, instructions
        FROM recipes
        WHERE mood = ?
        ORDER BY RANDOM()
        LIMIT 1
        """,
        (mood,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": f"No recipes found for mood '{mood}'."}), 404

    recipe = {
        "mood": row["mood"],
        "title": row["title"],
        "ingredients": row["ingredients"].split("\n"),
        "instructions": row["instructions"].split("\n"),
    }
    return jsonify({"recipe": recipe})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
