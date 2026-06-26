"""End-to-end recommendation pipeline."""

from __future__ import annotations

import pandas as pd

from src.data_loader import load_and_standardize
from src.feature_engineering import add_recipe_features
from src.preprocessing import preprocess_recipes
from src.scoring import build_explanation, compute_final_score, compute_ingredient_overlap
from src.similarity import compute_semantic_similarity


DISPLAY_COLUMNS = [
    "recipe_id",
    "recipe_name",
    "cuisine",
    "diet",
    "minutes",
    "rating",
    "review_count",
    "final_score",
    "semantic_similarity",
    "ingredient_overlap",
    "popularity_score",
    "cost_efficiency_score",
    "prep_efficiency_score",
    "margin_score",
    "matched_ingredients",
    "explanation",
]


def prepare_recipe_dataset(path: str | None = None) -> pd.DataFrame:
    """Load, clean, and feature-engineer recipes once per app session."""
    df = load_and_standardize(path)
    df = preprocess_recipes(df)
    return add_recipe_features(df)


def apply_filters(
    df: pd.DataFrame,
    max_prep_time: int | None = None,
    cuisine: str | None = None,
    diet: str | None = None,
) -> pd.DataFrame:
    """Apply optional UI filters before ranking."""
    filtered = df.copy()
    if max_prep_time:
        filtered = filtered[filtered["minutes_num"] <= max_prep_time]
    if cuisine and cuisine != "All":
        filtered = filtered[filtered["cuisine"].fillna("").str.lower() == cuisine.lower()]
    if diet and diet != "All":
        filtered = filtered[filtered["diet"].fillna("").str.lower() == diet.lower()]
    return filtered


def recommend_recipes(
    query: str,
    recipes: pd.DataFrame,
    top_n: int = 10,
    max_prep_time: int | None = None,
    cuisine: str | None = None,
    diet: str | None = None,
) -> pd.DataFrame:
    """Return top recipe candidates for a trend query."""
    if not query.strip():
        return pd.DataFrame(columns=DISPLAY_COLUMNS)

    candidates = apply_filters(recipes, max_prep_time, cuisine, diet).copy()
    if candidates.empty:
        return pd.DataFrame(columns=DISPLAY_COLUMNS)

    candidates["semantic_similarity"] = compute_semantic_similarity(candidates, query)
    candidates = compute_ingredient_overlap(candidates, query)
    candidates = compute_final_score(candidates)
    candidates["explanation"] = candidates.apply(build_explanation, axis=1)

    ranked = candidates.sort_values("final_score", ascending=False).head(top_n)
    available_columns = [column for column in DISPLAY_COLUMNS if column in ranked.columns]
    return ranked[available_columns].reset_index(drop=True)

