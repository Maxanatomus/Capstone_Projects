const moodSelect = document.getElementById("mood-select");
const getRecipeButton = document.getElementById("get-recipe");
const refreshRecipeButton = document.getElementById("refresh-recipe");
const recipeCard = document.getElementById("recipe-card");
const recipeTitle = document.getElementById("recipe-title");
const recipeMood = document.getElementById("recipe-mood");
const ingredientList = document.getElementById("ingredient-list");
const instructionList = document.getElementById("instruction-list");
const feedback = document.getElementById("feedback");

let lastMood = "";

const setLoadingState = (isLoading) => {
  const message = isLoading ? "Finding the perfect recipe..." : "Find Recipe";
  getRecipeButton.disabled = isLoading;
  getRecipeButton.textContent = message;
  refreshRecipeButton.disabled = isLoading;
};

const showFeedback = (message, isError = true) => {
  feedback.textContent = message;
  feedback.classList.toggle("hidden", !message);
  feedback.classList.toggle("text-rose-600", isError);
  feedback.classList.toggle("text-emerald-600", !isError);
};

const populateSelect = (moods) => {
  moods.forEach((mood) => {
    const option = document.createElement("option");
    option.value = mood;
    option.textContent = mood.charAt(0).toUpperCase() + mood.slice(1);
    moodSelect.appendChild(option);
  });
};

const fetchMoods = async () => {
  try {
    const response = await fetch("/api/moods");
    if (!response.ok) {
      throw new Error("Unable to load moods right now.");
    }
    const data = await response.json();
    populateSelect(data.moods);
  } catch (error) {
    showFeedback(error.message);
  }
};

const renderRecipe = (recipe) => {
  recipeTitle.textContent = recipe.title;
  recipeMood.textContent = `Mood: ${recipe.mood}`;

  ingredientList.innerHTML = "";
  recipe.ingredients.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    ingredientList.appendChild(li);
  });

  instructionList.innerHTML = "";
  recipe.instructions.forEach((step) => {
    const li = document.createElement("li");
    li.textContent = step;
    instructionList.appendChild(li);
  });

  recipeCard.classList.remove("hidden");
};

const fetchRecipe = async (mood) => {
  setLoadingState(true);
  showFeedback("");
  try {
    const response = await fetch(`/api/recipe?mood=${encodeURIComponent(mood)}`);
    if (!response.ok) {
      const { error } = await response.json();
      throw new Error(error || "Unable to load a recipe right now.");
    }
    const data = await response.json();
    renderRecipe(data.recipe);
    lastMood = mood;
  } catch (error) {
    showFeedback(error.message);
  } finally {
    setLoadingState(false);
  }
};

getRecipeButton.addEventListener("click", () => {
  const mood = moodSelect.value;
  if (!mood) {
    showFeedback("Please pick a mood first.");
    return;
  }
  fetchRecipe(mood);
});

refreshRecipeButton.addEventListener("click", () => {
  if (lastMood) {
    fetchRecipe(lastMood);
  } else {
    showFeedback("Choose a mood and grab a recipe first.");
  }
});

fetchMoods();
