import sqlite3
import json

def init_db():
    """Initialize the database with recipes table and seed data"""
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    
    # Create recipes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mood TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            prep_time TEXT,
            difficulty TEXT
        )
    ''')
    
    # Check if we already have data
    cursor.execute('SELECT COUNT(*) FROM recipes')
    if cursor.fetchone()[0] == 0:
        # Seed with mood-based recipes
        recipes = [
            # Happy mood recipes
            {
                'name': 'Rainbow Veggie Buddha Bowl',
                'mood': 'happy',
                'ingredients': json.dumps([
                    '1 cup quinoa',
                    '1 cup chickpeas',
                    '1 avocado',
                    '1 cup cherry tomatoes',
                    '1 cup shredded carrots',
                    '2 cups mixed greens',
                    'Tahini dressing'
                ]),
                'instructions': '1. Cook quinoa according to package instructions.\n2. Roast chickpeas with olive oil and spices at 400°F for 20 minutes.\n3. Arrange quinoa, chickpeas, sliced avocado, tomatoes, carrots, and greens in a bowl.\n4. Drizzle with tahini dressing and enjoy!',
                'prep_time': '30 minutes',
                'difficulty': 'Easy'
            },
            {
                'name': 'Tropical Fruit Smoothie Bowl',
                'mood': 'happy',
                'ingredients': json.dumps([
                    '2 frozen bananas',
                    '1 cup frozen mango',
                    '1/2 cup coconut milk',
                    '1 tbsp honey',
                    'Toppings: granola, fresh berries, coconut flakes'
                ]),
                'instructions': '1. Blend frozen bananas, mango, coconut milk, and honey until smooth.\n2. Pour into a bowl.\n3. Top with granola, fresh berries, and coconut flakes.\n4. Serve immediately!',
                'prep_time': '10 minutes',
                'difficulty': 'Easy'
            },
            {
                'name': 'Lemon Herb Grilled Chicken',
                'mood': 'happy',
                'ingredients': json.dumps([
                    '4 chicken breasts',
                    '3 tbsp olive oil',
                    '2 lemons (juice and zest)',
                    '3 cloves garlic',
                    'Fresh herbs (thyme, rosemary)',
                    'Salt and pepper'
                ]),
                'instructions': '1. Mix olive oil, lemon juice, zest, minced garlic, and herbs in a bowl.\n2. Marinate chicken for at least 30 minutes.\n3. Grill chicken for 6-7 minutes per side until cooked through.\n4. Serve with your favorite sides!',
                'prep_time': '45 minutes',
                'difficulty': 'Medium'
            },
            # Sad mood recipes (comfort food)
            {
                'name': 'Classic Mac and Cheese',
                'mood': 'sad',
                'ingredients': json.dumps([
                    '1 lb elbow macaroni',
                    '4 cups shredded cheddar cheese',
                    '3 cups milk',
                    '4 tbsp butter',
                    '1/4 cup flour',
                    'Salt and pepper',
                    'Breadcrumbs (optional)'
                ]),
                'instructions': '1. Cook pasta according to package directions.\n2. Melt butter in a large pot, add flour and whisk for 1 minute.\n3. Slowly add milk, stirring constantly until thickened.\n4. Add cheese and stir until melted.\n5. Mix in cooked pasta.\n6. Optional: Top with breadcrumbs and bake at 350°F for 20 minutes.',
                'prep_time': '40 minutes',
                'difficulty': 'Medium'
            },
            {
                'name': 'Warm Chocolate Chip Cookies',
                'mood': 'sad',
                'ingredients': json.dumps([
                    '2 1/4 cups flour',
                    '1 cup butter (softened)',
                    '3/4 cup sugar',
                    '3/4 cup brown sugar',
                    '2 eggs',
                    '2 tsp vanilla',
                    '1 tsp baking soda',
                    '2 cups chocolate chips'
                ]),
                'instructions': '1. Preheat oven to 375°F.\n2. Cream together butter and sugars.\n3. Beat in eggs and vanilla.\n4. Mix in flour and baking soda.\n5. Fold in chocolate chips.\n6. Drop spoonfuls onto baking sheet.\n7. Bake for 9-11 minutes.\n8. Let cool slightly and enjoy warm!',
                'prep_time': '25 minutes',
                'difficulty': 'Easy'
            },
            {
                'name': 'Creamy Tomato Soup',
                'mood': 'sad',
                'ingredients': json.dumps([
                    '2 cans crushed tomatoes',
                    '1 cup heavy cream',
                    '1 onion (diced)',
                    '4 cloves garlic',
                    '2 cups vegetable broth',
                    'Fresh basil',
                    'Olive oil, salt, pepper'
                ]),
                'instructions': '1. Sauté onion and garlic in olive oil until soft.\n2. Add crushed tomatoes and vegetable broth.\n3. Simmer for 15 minutes.\n4. Blend until smooth using an immersion blender.\n5. Stir in heavy cream and basil.\n6. Season with salt and pepper.\n7. Serve hot with grilled cheese!',
                'prep_time': '30 minutes',
                'difficulty': 'Easy'
            },
            # Stressed mood recipes (quick and easy)
            {
                'name': '15-Minute Garlic Shrimp Pasta',
                'mood': 'stressed',
                'ingredients': json.dumps([
                    '12 oz spaghetti',
                    '1 lb shrimp (peeled)',
                    '6 cloves garlic',
                    '1/4 cup olive oil',
                    'Red pepper flakes',
                    'Fresh parsley',
                    'Lemon juice',
                    'Salt and pepper'
                ]),
                'instructions': '1. Cook pasta according to package directions.\n2. Heat olive oil in a large pan.\n3. Add minced garlic and red pepper flakes, cook for 1 minute.\n4. Add shrimp and cook until pink (3-4 minutes).\n5. Toss with cooked pasta, lemon juice, and parsley.\n6. Season and serve!',
                'prep_time': '15 minutes',
                'difficulty': 'Easy'
            },
            {
                'name': 'Quick Veggie Stir Fry',
                'mood': 'stressed',
                'ingredients': json.dumps([
                    '2 cups mixed vegetables',
                    '2 tbsp soy sauce',
                    '1 tbsp sesame oil',
                    '2 cloves garlic',
                    '1 tsp ginger',
                    'Cooked rice',
                    'Sesame seeds'
                ]),
                'instructions': '1. Heat sesame oil in a wok or large pan.\n2. Add minced garlic and ginger, stir for 30 seconds.\n3. Add vegetables and stir-fry for 5-7 minutes.\n4. Add soy sauce and toss to coat.\n5. Serve over rice and sprinkle with sesame seeds.',
                'prep_time': '15 minutes',
                'difficulty': 'Easy'
            },
            {
                'name': 'Avocado Toast with Egg',
                'mood': 'stressed',
                'ingredients': json.dumps([
                    '2 slices whole grain bread',
                    '1 ripe avocado',
                    '2 eggs',
                    'Cherry tomatoes',
                    'Feta cheese',
                    'Red pepper flakes',
                    'Salt and pepper'
                ]),
                'instructions': '1. Toast bread until golden.\n2. Mash avocado and spread on toast.\n3. Cook eggs to your liking (fried or poached).\n4. Top toast with eggs, halved cherry tomatoes, and feta.\n5. Season with salt, pepper, and red pepper flakes.',
                'prep_time': '10 minutes',
                'difficulty': 'Easy'
            },
            # Energetic mood recipes (high energy foods)
            {
                'name': 'Protein Power Breakfast Bowl',
                'mood': 'energetic',
                'ingredients': json.dumps([
                    '2 eggs',
                    '1/2 cup black beans',
                    '1/2 avocado',
                    '1/4 cup salsa',
                    '2 tbsp Greek yogurt',
                    'Handful of spinach',
                    'Hot sauce (optional)'
                ]),
                'instructions': '1. Scramble eggs in a pan.\n2. Warm black beans.\n3. Arrange eggs, beans, sliced avocado, and spinach in a bowl.\n4. Top with salsa, Greek yogurt, and hot sauce.\n5. Enjoy this protein-packed meal!',
                'prep_time': '15 minutes',
                'difficulty': 'Easy'
            },
            {
                'name': 'Thai Peanut Chicken Wraps',
                'mood': 'energetic',
                'ingredients': json.dumps([
                    '2 cups cooked chicken (shredded)',
                    '1/4 cup peanut butter',
                    '2 tbsp soy sauce',
                    '1 tbsp honey',
                    'Lime juice',
                    'Tortillas',
                    'Shredded cabbage',
                    'Carrots',
                    'Cilantro'
                ]),
                'instructions': '1. Mix peanut butter, soy sauce, honey, and lime juice to make sauce.\n2. Toss chicken with half the sauce.\n3. Fill tortillas with chicken, cabbage, shredded carrots, and cilantro.\n4. Drizzle with remaining sauce.\n5. Roll up and enjoy!',
                'prep_time': '20 minutes',
                'difficulty': 'Easy'
            },
            {
                'name': 'Mediterranean Quinoa Salad',
                'mood': 'energetic',
                'ingredients': json.dumps([
                    '2 cups cooked quinoa',
                    '1 cucumber (diced)',
                    '1 cup cherry tomatoes',
                    '1/2 cup feta cheese',
                    '1/4 cup olives',
                    '1/4 cup red onion',
                    'Olive oil and lemon dressing',
                    'Fresh mint and parsley'
                ]),
                'instructions': '1. Let cooked quinoa cool.\n2. Combine quinoa, cucumber, halved tomatoes, feta, olives, and red onion.\n3. Make dressing with olive oil, lemon juice, salt, and pepper.\n4. Toss salad with dressing.\n5. Add fresh herbs and serve!',
                'prep_time': '25 minutes',
                'difficulty': 'Easy'
            },
            # Relaxed mood recipes (light and fresh)
            {
                'name': 'Caprese Salad',
                'mood': 'relaxed',
                'ingredients': json.dumps([
                    '3 large tomatoes',
                    '8 oz fresh mozzarella',
                    'Fresh basil leaves',
                    'Balsamic glaze',
                    'Extra virgin olive oil',
                    'Sea salt and pepper'
                ]),
                'instructions': '1. Slice tomatoes and mozzarella into 1/4 inch rounds.\n2. Arrange alternating slices on a platter.\n3. Tuck basil leaves between slices.\n4. Drizzle with olive oil and balsamic glaze.\n5. Season with sea salt and freshly cracked pepper.\n6. Serve at room temperature.',
                'prep_time': '10 minutes',
                'difficulty': 'Easy'
            },
            {
                'name': 'Herbed Salmon with Asparagus',
                'mood': 'relaxed',
                'ingredients': json.dumps([
                    '4 salmon fillets',
                    '1 bunch asparagus',
                    '3 tbsp olive oil',
                    '2 cloves garlic',
                    'Fresh dill',
                    'Lemon slices',
                    'Salt and pepper'
                ]),
                'instructions': '1. Preheat oven to 400°F.\n2. Place salmon and asparagus on a baking sheet.\n3. Brush with olive oil and minced garlic.\n4. Top salmon with dill and lemon slices.\n5. Season everything with salt and pepper.\n6. Bake for 12-15 minutes until salmon is cooked through.',
                'prep_time': '25 minutes',
                'difficulty': 'Medium'
            },
            {
                'name': 'Green Tea Infused Rice Bowl',
                'mood': 'relaxed',
                'ingredients': json.dumps([
                    '2 cups jasmine rice',
                    '2 green tea bags',
                    'Edamame',
                    'Cucumber',
                    'Avocado',
                    'Pickled ginger',
                    'Sesame seeds',
                    'Soy sauce'
                ]),
                'instructions': '1. Brew strong green tea and use it to cook rice.\n2. Let rice cool to room temperature.\n3. Top with edamame, sliced cucumber, avocado, and pickled ginger.\n4. Sprinkle with sesame seeds.\n5. Serve with soy sauce on the side.',
                'prep_time': '30 minutes',
                'difficulty': 'Easy'
            }
        ]
        
        for recipe in recipes:
            cursor.execute('''
                INSERT INTO recipes (name, mood, ingredients, instructions, prep_time, difficulty)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (recipe['name'], recipe['mood'], recipe['ingredients'], 
                  recipe['instructions'], recipe['prep_time'], recipe['difficulty']))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_recipe_by_mood(mood):
    """Get a random recipe for a specific mood"""
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM recipes 
        WHERE mood = ? 
        ORDER BY RANDOM() 
        LIMIT 1
    ''', (mood,))
    
    recipe = cursor.fetchone()
    conn.close()
    
    if recipe:
        return {
            'id': recipe['id'],
            'name': recipe['name'],
            'mood': recipe['mood'],
            'ingredients': json.loads(recipe['ingredients']),
            'instructions': recipe['instructions'],
            'prep_time': recipe['prep_time'],
            'difficulty': recipe['difficulty']
        }
    return None

if __name__ == '__main__':
    init_db()
