// API base URL
const API_BASE = window.location.origin;

// Store current mood
let currentMood = null;

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    loadMoodButtons();
});

// Load mood buttons from API
async function loadMoodButtons() {
    try {
        const response = await fetch(`${API_BASE}/api/moods`);
        const moods = await response.json();
        
        const moodButtonsContainer = document.getElementById('mood-buttons');
        moodButtonsContainer.innerHTML = '';
        
        moods.forEach(mood => {
            const button = document.createElement('button');
            button.className = 'mood-button bg-gradient-to-br from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold py-6 px-4 rounded-xl shadow-md text-center';
            button.innerHTML = `
                <div class="text-4xl mb-2">${mood.emoji}</div>
                <div class="text-lg">${mood.label.split(' ')[1]}</div>
            `;
            button.onclick = () => selectMood(mood.value);
            moodButtonsContainer.appendChild(button);
        });
    } catch (error) {
        showError('Failed to load moods. Please refresh the page.');
    }
}

// Handle mood selection
async function selectMood(mood) {
    currentMood = mood;
    
    // Highlight selected mood button
    const buttons = document.querySelectorAll('.mood-button');
    buttons.forEach(btn => btn.classList.remove('selected'));
    event.target.closest('.mood-button').classList.add('selected');
    
    // Get recipe for selected mood
    await getRecipe(mood);
}

// Fetch and display recipe
async function getRecipe(mood) {
    // Show loading
    document.getElementById('mood-section').classList.add('hidden');
    document.getElementById('recipe-section').classList.add('hidden');
    document.getElementById('error-section').classList.add('hidden');
    document.getElementById('loading').classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_BASE}/api/recipe/${mood}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch recipe');
        }
        
        const recipe = await response.json();
        displayRecipe(recipe);
        
        // Hide loading, show recipe
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('recipe-section').classList.remove('hidden');
    } catch (error) {
        document.getElementById('loading').classList.add('hidden');
        showError('Failed to load recipe. Please try again.');
    }
}

// Display recipe details
function displayRecipe(recipe) {
    document.getElementById('recipe-name').textContent = recipe.name;
    document.getElementById('recipe-time').innerHTML = `
        <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        ${recipe.prep_time}
    `;
    document.getElementById('recipe-difficulty').innerHTML = `
        <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
        </svg>
        ${recipe.difficulty}
    `;
    
    // Display ingredients
    const ingredientsList = document.getElementById('recipe-ingredients');
    ingredientsList.innerHTML = '';
    recipe.ingredients.forEach(ingredient => {
        const li = document.createElement('li');
        li.className = 'flex items-start';
        li.innerHTML = `
            <svg class="w-5 h-5 mr-2 mt-0.5 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
            </svg>
            <span class="text-gray-700">${ingredient}</span>
        `;
        ingredientsList.appendChild(li);
    });
    
    // Display instructions
    document.getElementById('recipe-instructions').textContent = recipe.instructions;
}

// Get a new recipe with the same mood
function getNewRecipe() {
    if (currentMood) {
        getRecipe(currentMood);
    }
}

// Change mood and go back to selection
function changeMood() {
    currentMood = null;
    document.getElementById('recipe-section').classList.add('hidden');
    document.getElementById('mood-section').classList.remove('hidden');
    
    // Remove selected state from all buttons
    const buttons = document.querySelectorAll('.mood-button');
    buttons.forEach(btn => btn.classList.remove('selected'));
}

// Show error message
function showError(message) {
    const errorSection = document.getElementById('error-section');
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
    
    // Hide error after 5 seconds
    setTimeout(() => {
        errorSection.classList.add('hidden');
    }, 5000);
}
