"""Data loading utilities for recipe recommendation experiments.

The loader accepts flexible column mappings so the same MVP can work with
Food.com, Epicurious, or an internal recipe export after a small config change.
"""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

import pandas as pd


DEFAULT_COLUMN_MAP = {
    "recipe_id": ["recipe_id", "id"],
    "recipe_name": ["recipe_name", "name", "title"],
    "ingredients": ["ingredients", "ingredient_list"],
    "tags": ["tags", "categories"],
    "steps": ["steps", "instructions", "directions"],
    "minutes": ["minutes", "prep_time_minutes", "cook_time", "total_time"],
    "nutrition": ["nutrition"],
    "n_steps": ["n_steps", "step_count"],
    "n_ingredients": ["n_ingredients", "ingredient_count"],
    "rating": ["rating", "avg_rating", "mean_rating"],
    "review_count": ["review_count", "n_reviews", "num_reviews"],
    "cost": ["cost", "estimated_cost", "food_cost"],
    "margin": ["margin", "gross_margin", "profit_margin"],
    "cuisine": ["cuisine", "cuisine_type"],
    "diet": ["diet", "diet_type"],
}


def load_recipe_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load a recipe CSV or return a small built-in sample dataset.

    Parameters
    ----------
    path:
        CSV file path. If omitted or missing, the function returns sample data
        so the app can be launched before a Kaggle dataset is downloaded.
    """
    if path is None:
        return load_sample_data()

    path = Path(path)
    if not path.exists():
        return load_sample_data()

    if path.suffix.lower() != ".csv":
        raise ValueError("This MVP loader currently supports CSV files only.")

    return pd.read_csv(path)


def standardize_columns(
    df: pd.DataFrame,
    column_map: Mapping[str, list[str]] | None = None,
) -> pd.DataFrame:
    """Rename available dataset columns to the canonical names used by src.

    Missing canonical fields are created with sensible empty defaults, which
    keeps downstream code stable while you map real Kaggle columns later.
    """
    column_map = column_map or DEFAULT_COLUMN_MAP
    rename_lookup = {}
    lower_to_original = {column.lower(): column for column in df.columns}

    for canonical, candidates in column_map.items():
        if canonical in df.columns:
            continue
        for candidate in candidates:
            original = lower_to_original.get(candidate.lower())
            if original is not None:
                rename_lookup[original] = canonical
                break

    standardized = df.rename(columns=rename_lookup).copy()

    defaults = {
        "recipe_id": range(1, len(standardized) + 1),
        "recipe_name": "",
        "ingredients": "",
        "tags": "",
        "steps": "",
        "minutes": None,
        "nutrition": "",
        "n_steps": None,
        "n_ingredients": None,
        "rating": None,
        "review_count": None,
        "cost": None,
        "margin": None,
        "cuisine": "",
        "diet": "",
    }
    for column, default in defaults.items():
        if column not in standardized.columns:
            standardized[column] = default

    return standardized


def load_and_standardize(path: str | Path | None = None) -> pd.DataFrame:
    """Convenience wrapper used by the Streamlit app and quick scripts."""
    return standardize_columns(load_recipe_data(path))


def load_sample_data() -> pd.DataFrame:
    """Small demo dataset for local smoke tests and portfolio screenshots."""
    return pd.DataFrame(
        [
            {
                "recipe_id": 1,
                "recipe_name": "Herbed Flatbread with Tomato and Mozzarella",
                "ingredients": "flatbread, tomato sauce, mozzarella, basil, olive oil",
                "tags": "italian, vegetarian, quick",
                "steps": "Top flatbread with tomato sauce and mozzarella. Bake until crisp. Finish with basil.",
                "minutes": 22,
                "n_steps": 3,
                "n_ingredients": 5,
                "rating": 4.7,
                "review_count": 128,
                "cost": 4.2,
                "margin": 0.68,
                "cuisine": "Italian",
                "diet": "Vegetarian",
            },
            {
                "recipe_id": 2,
                "recipe_name": "Spicy Kimchi Quesadilla",
                "ingredients": "tortilla, kimchi, cheddar, scallions, gochujang mayo",
                "tags": "korean, fusion, spicy",
                "steps": "Layer kimchi and cheese in a tortilla. Toast until melted. Serve with gochujang mayo.",
                "minutes": 18,
                "n_steps": 4,
                "n_ingredients": 5,
                "rating": 4.5,
                "review_count": 89,
                "cost": 3.6,
                "margin": 0.72,
                "cuisine": "Korean Fusion",
                "diet": "",
            },
            {
                "recipe_id": 3,
                "recipe_name": "Cauliflower Crust Veggie Bake",
                "ingredients": "cauliflower, egg, parmesan, marinara, bell pepper, mushrooms",
                "tags": "low carb, vegetarian, baked",
                "steps": "Press cauliflower crust, bake, add marinara and vegetables, then bake again.",
                "minutes": 50,
                "n_steps": 8,
                "n_ingredients": 6,
                "rating": 4.2,
                "review_count": 52,
                "cost": 5.1,
                "margin": 0.61,
                "cuisine": "American",
                "diet": "Vegetarian",
            },
            {
                "recipe_id": 4,
                "recipe_name": "Buffalo Chicken Dip",
                "ingredients": "chicken, cream cheese, buffalo sauce, cheddar, ranch",
                "tags": "party, american, high protein",
                "steps": "Combine shredded chicken with sauces and cheese. Bake until bubbling.",
                "minutes": 30,
                "n_steps": 5,
                "n_ingredients": 5,
                "rating": 4.8,
                "review_count": 220,
                "cost": 6.8,
                "margin": 0.58,
                "cuisine": "American",
                "diet": "",
            },
            {
                "recipe_id": 5,
                "recipe_name": "Mediterranean Chickpea Bowl",
                "ingredients": "chickpeas, cucumber, tomato, feta, tahini, lemon, parsley",
                "tags": "mediterranean, healthy, vegetarian",
                "steps": "Build a bowl with chickpeas, chopped vegetables, feta, herbs, and tahini lemon sauce.",
                "minutes": 15,
                "n_steps": 3,
                "n_ingredients": 7,
                "rating": 4.6,
                "review_count": 156,
                "cost": 3.9,
                "margin": 0.70,
                "cuisine": "Mediterranean",
                "diet": "Vegetarian",
            },
            {
                "recipe_id": 6,
                "recipe_name": "Garlic Mushroom Toast",
                "ingredients": "sourdough, mushrooms, garlic, thyme, butter, parmesan",
                "tags": "brunch, vegetarian, savory",
                "steps": "Saute mushrooms with garlic and thyme. Spoon over toasted sourdough with parmesan.",
                "minutes": 20,
                "n_steps": 4,
                "n_ingredients": 6,
                "rating": 4.4,
                "review_count": 74,
                "cost": 4.0,
                "margin": 0.65,
                "cuisine": "European",
                "diet": "Vegetarian",
            },
        ]
    )

