"""Streamlit dashboard for the AI-Powered Menu Trend Recommendation System."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.recommender import prepare_recipe_dataset, recommend_recipes
from src.trend_expansion import expand_trend_query


PROJECT_ROOT = Path(__file__).parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "recipes.csv"


st.set_page_config(
    page_title="Menu Trend Recommender",
    page_icon="🍕",
    layout="wide",
)


@st.cache_data(show_spinner="Loading and engineering recipe features...")
def load_recipes(data_path: str | None) -> pd.DataFrame:
    """Cache preprocessing so repeated queries stay fast."""
    return prepare_recipe_dataset(data_path)


def score_bar_chart(row: pd.Series) -> plt.Figure:
    """Create a compact score-breakdown bar chart."""
    score_columns = [
        "semantic_similarity",
        "ingredient_overlap",
        "popularity_score",
        "cost_efficiency_score",
        "prep_efficiency_score",
        "margin_score",
    ]
    labels = [
        "Semantic",
        "Ingredients",
        "Popularity",
        "Cost",
        "Prep",
        "Margin",
    ]
    values = [float(row.get(column, 0)) for column in score_columns]

    fig, ax = plt.subplots(figsize=(6, 2.4))
    ax.barh(labels, values, color=["#2563eb", "#16a34a", "#f59e0b", "#0f766e", "#7c3aed", "#dc2626"])
    ax.set_xlim(0, 1)
    ax.set_xlabel("Score")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    return fig


st.title("AI-Powered Menu Trend Recommendation System")
st.caption(
    "A data science MVP that combines semantic similarity, ingredient overlap, "
    "and business scoring to recommend adaptable recipes for new menu ideas."
)

with st.sidebar:
    st.header("Dataset")
    data_path = st.text_input(
        "Recipe CSV path",
        value=str(DEFAULT_DATA_PATH) if DEFAULT_DATA_PATH.exists() else "",
        help="Leave blank to use the built-in sample dataset.",
    )
    recipes = load_recipes(data_path.strip() or None)

    st.metric("Recipes loaded", f"{len(recipes):,}")

    st.header("Filters")
    max_prep_time = st.slider("Max prep time", min_value=5, max_value=180, value=90, step=5)

    cuisine_options = ["All"] + sorted(
        cuisine for cuisine in recipes["cuisine"].dropna().astype(str).unique() if cuisine
    )
    diet_options = ["All"] + sorted(
        diet for diet in recipes["diet"].dropna().astype(str).unique() if diet
    )
    cuisine = st.selectbox("Cuisine", cuisine_options)
    diet = st.selectbox("Diet", diet_options)
    top_n = st.radio("Number of recommendations", [5, 10], horizontal=True, index=0)

query = st.text_input(
    "Trend keyword or business question",
    value="Pizza is trending. Which existing recipes could be adapted into pizza-related menu items?",
)

expanded = expand_trend_query(query)
if expanded["ingredients"]:
    st.write("Trend ingredients detected:", ", ".join(expanded["ingredients"]))

recommendations = recommend_recipes(
    query=query,
    recipes=recipes,
    top_n=top_n,
    max_prep_time=max_prep_time,
    cuisine=cuisine,
    diet=diet,
)

if recommendations.empty:
    st.warning("No recommendations found. Try relaxing the filters or entering a trend query.")
    st.stop()

summary_columns = [
    "recipe_name",
    "final_score",
    "semantic_similarity",
    "ingredient_overlap",
    "popularity_score",
    "prep_efficiency_score",
]
st.subheader("Top Recipe Candidates")
st.dataframe(
    recommendations[summary_columns].style.format(
        {
            "final_score": "{:.3f}",
            "semantic_similarity": "{:.3f}",
            "ingredient_overlap": "{:.3f}",
            "popularity_score": "{:.3f}",
            "prep_efficiency_score": "{:.3f}",
        }
    ),
    use_container_width=True,
)

st.download_button(
    "Download recommendations CSV",
    data=recommendations.to_csv(index=False).encode("utf-8"),
    file_name="menu_trend_recommendations.csv",
    mime="text/csv",
)

st.subheader("Recommendation Explanations")
for _, row in recommendations.iterrows():
    with st.expander(f"{row['recipe_name']} | Final score {row['final_score']:.3f}", expanded=False):
        left, right = st.columns([1.2, 1])
        with left:
            st.write(row["explanation"])
            st.write("Matched ingredients:", ", ".join(row["matched_ingredients"]) or "None")
            st.write(
                {
                    "recipe_id": row["recipe_id"],
                    "cuisine": row.get("cuisine", ""),
                    "diet": row.get("diet", ""),
                    "minutes": row.get("minutes", ""),
                    "rating": row.get("rating", ""),
                    "review_count": row.get("review_count", ""),
                }
            )
        with right:
            st.pyplot(score_bar_chart(row), clear_figure=True)

st.subheader("Model Positioning")
st.write(
    "This MVP is intentionally framed as a ranking system: recipe text is embedded for "
    "semantic retrieval, trend ingredients are matched with engineered ingredient lists, "
    "and normalized business features are blended into a weighted recommendation score."
)

