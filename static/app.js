let currentMood = null;
let currentRecipeId = null;

// Mood selection buttons
const moodButtons = document.querySelectorAll('.mood-btn');
const moodSelection = document.getElementById('mood-selection');
const recipeDisplay = document.getElementById('recipe-display');
const loading = document.getElementById('loading');
const newRecipeBtn = document.getElementById('new-recipe-btn');
const backBtn = document.getElementById('back-btn');

// Add click handlers to mood buttons
moodButtons.forEach(button => {
    button.addEventListener('click', () => {
        const mood = button.getAttribute('data-mood');
        selectMood(mood);
    });
});

// Select mood and fetch recipe
async function selectMood(mood) {
    currentMood = mood;
    currentRecipeId = null;
    
    // Update UI
    moodButtons.forEach(btn => {
        if (btn.getAttribute('data-mood') === mood) {
            btn.classList.add('selected');
        } else {
            btn.classList.remove('selected');
        }
    });
    
    // Show loading, hide selection
    moodSelection.classList.add('hidden');
    loading.classList.remove('hidden');
    recipeDisplay.classList.add('hidden');
    
    // Fetch recipe
    await fetchRecipe(mood);
}

// Fetch recipe from API
async function fetchRecipe(mood, excludeId = null) {
    try {
        let url = `/api/recipe?mood=${mood}`;
        if (excludeId) {
            url += `&exclude_id=${excludeId}`;
        }
        
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error('Failed to fetch recipe');
        }
        
        const recipe = await response.json();
        displayRecipe(recipe);
    } catch (error) {
        console.error('Error fetching recipe:', error);
        alert('Failed to fetch recipe. Please try again.');
        // Show mood selection again
        loading.classList.add('hidden');
        moodSelection.classList.remove('hidden');
    }
}

// Display recipe
function displayRecipe(recipe) {
    currentRecipeId = recipe.id;
    
    document.getElementById('recipe-name').textContent = recipe.name;
    document.getElementById('recipe-description').textContent = recipe.description || '';
    
    // Format ingredients
    const ingredientsList = document.getElementById('recipe-ingredients');
    ingredientsList.innerHTML = '';
    const ingredients = recipe.ingredients.split(',').map(ing => ing.trim());
    ingredients.forEach(ingredient => {
        const li = document.createElement('li');
        li.textContent = ingredient;
        ingredientsList.appendChild(li);
    });
    
    // Display instructions
    document.getElementById('recipe-instructions').textContent = recipe.instructions;
    
    // Show recipe, hide loading
    loading.classList.add('hidden');
    recipeDisplay.classList.remove('hidden');
}

// Get another recipe for the same mood
newRecipeBtn.addEventListener('click', async () => {
    if (!currentMood) return;
    
    loading.classList.remove('hidden');
    recipeDisplay.classList.add('hidden');
    
    await fetchRecipe(currentMood, currentRecipeId);
});

// Back to mood selection
backBtn.addEventListener('click', () => {
    recipeDisplay.classList.add('hidden');
    moodSelection.classList.remove('hidden');
    
    // Reset selected mood button
    moodButtons.forEach(btn => btn.classList.remove('selected'));
    currentMood = null;
    currentRecipeId = null;
});
