# AI-Powered Menu Trend Recommendation System

This is a data science portfolio MVP for recommending existing recipes that can be adapted into trend-driven menu ideas.

Example question:

```text
Pizza is trending. Which existing recipes in our database could be reused or adapted into pizza-related menu items?
```

The project is positioned as a recommendation and ranking system, not a chatbot. It uses feature engineering, semantic similarity, ingredient overlap, business scoring, explainability, and a simple Streamlit dashboard.

## Project Structure

```text
menu-trend-recommender/
├── README.md
├── requirements.txt
├── app.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_eda.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── trend_expansion.py
│   ├── similarity.py
│   ├── scoring.py
│   ├── recommender.py
│   └── evaluation.py
└── outputs/
    └── sample_recommendations.csv
```

## MVP Features

- Flexible recipe CSV loading with column standardization.
- Beginner-friendly preprocessing for ingredients, tags, instructions, and recipe text.
- Recipe-level feature engineering for popularity, prep efficiency, cost efficiency, and margin.
- Trend keyword expansion dictionary for ingredients and related concepts.
- Semantic similarity using `sentence-transformers`.
- TF-IDF fallback if a transformer model is unavailable in the local environment.
- Ingredient overlap scoring between trend ingredients and recipe ingredients.
- Weighted final recommendation score:

```text
final_score =
0.35 * semantic_similarity
+ 0.25 * ingredient_overlap
+ 0.15 * popularity_score
+ 0.10 * cost_efficiency
+ 0.10 * prep_efficiency
+ 0.05 * margin_score
```

## Dataset

Place your Kaggle recipe CSV at:

```text
data/raw/recipes.csv
```

The code assumes the dataset may contain columns like:

- `recipe_id`
- `recipe_name`
- `ingredients`
- `tags`
- `steps` or `instructions`
- `minutes` or `prep_time_minutes`
- `nutrition`
- `n_steps`
- `n_ingredients`
- `rating` or `avg_rating`
- `review_count`

If the column names differ, update `DEFAULT_COLUMN_MAP` in `src/data_loader.py`.

If no CSV is available, the app uses a small built-in sample dataset so the MVP still runs.

## Cost and Margin Placeholder Logic

Many public recipe datasets do not include ingredient cost, selling price, or margin. This MVP handles those gaps explicitly:

- If `cost` exists, lower cost receives a higher `cost_efficiency_score`.
- If `cost` is missing, `cost_efficiency_score` defaults to `0.5`, a neutral placeholder.
- If `margin` exists, higher margin receives a higher `margin_score`.
- If `margin` is missing, `margin_score` defaults to `0.5`, a neutral placeholder.

For a production version, cost could be estimated by joining ingredients to supplier prices, and margin could be calculated from expected menu price minus estimated food cost.

## How to Run Locally

From the project folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Quick Python Usage

```python
from src.recommender import prepare_recipe_dataset, recommend_recipes

recipes = prepare_recipe_dataset("data/raw/recipes.csv")
results = recommend_recipes(
    query="Pizza is trending. Which recipes could become pizza-inspired menu items?",
    recipes=recipes,
    top_n=10,
)
print(results[["recipe_name", "final_score", "explanation"]])
```

## Evaluation Ideas

For a stronger portfolio story, add evaluation in phases:

- Create a manually labeled validation set of trend queries and relevant recipes.
- Measure Precision@K and Recall@K.
- Track score distribution and recommendation diversity.
- Compare ranking variants:
  - semantic-only
  - ingredient-only
  - business-only
  - full weighted model
- Collect qualitative feedback from chefs, menu planners, or product managers.

## Next Improvements

- Add automatic trend extraction from Google Trends, TikTok food trends, or internal sales data.
- Replace static keyword expansion with an LLM-assisted trend-to-ingredient parser.
- Add ingredient substitution suggestions.
- Add SQLite or DuckDB for larger recipe catalogs.
- Add model cards and experiment tracking.

