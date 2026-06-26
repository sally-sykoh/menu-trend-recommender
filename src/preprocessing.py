"""Text and ingredient preprocessing helpers."""

from __future__ import annotations

import ast
import re
from typing import Iterable

import pandas as pd


TOKEN_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z\s\-']+")


def normalize_text(value: object) -> str:
    """Convert lists, nulls, and raw strings into clean lowercase text."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
    return re.sub(r"\s+", " ", str(value).lower()).strip()


def parse_list_like(value: object) -> list[str]:
    """Parse common Kaggle list-like strings into a list of clean tokens."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        raw_items = value
    else:
        text = str(value).strip()
        try:
            parsed = ast.literal_eval(text)
            raw_items = parsed if isinstance(parsed, list) else [text]
        except (ValueError, SyntaxError):
            raw_items = re.split(r",|;", text)

    return [normalize_text(item) for item in raw_items if normalize_text(item)]


def clean_ingredient_name(ingredient: str) -> str:
    """Remove quantities and light descriptors from ingredient names."""
    ingredient = normalize_text(ingredient)
    ingredient = re.sub(r"\b\d+([./]\d+)?\b", " ", ingredient)
    ingredient = re.sub(
        r"\b(cup|cups|tbsp|tablespoon|tsp|teaspoon|oz|ounce|ounces|g|gram|grams|kg|ml|lb|lbs)\b",
        " ",
        ingredient,
    )
    ingredient = re.sub(r"[^a-z\s\-']", " ", ingredient)
    return re.sub(r"\s+", " ", ingredient).strip()


def preprocess_recipes(df: pd.DataFrame) -> pd.DataFrame:
    """Add normalized ingredient, tag, step, and combined text columns."""
    processed = df.copy()
    processed["ingredient_list"] = processed["ingredients"].apply(parse_list_like)
    processed["clean_ingredients"] = processed["ingredient_list"].apply(
        lambda items: [clean_ingredient_name(item) for item in items if clean_ingredient_name(item)]
    )
    processed["tag_list"] = processed["tags"].apply(parse_list_like)
    processed["recipe_text"] = processed.apply(build_recipe_text, axis=1)
    return processed


def build_recipe_text(row: pd.Series) -> str:
    """Create one text field for semantic matching."""
    parts: Iterable[str] = [
        normalize_text(row.get("recipe_name", "")),
        " ".join(row.get("clean_ingredients", []) or []),
        " ".join(row.get("tag_list", []) or []),
        normalize_text(row.get("steps", "")),
    ]
    return " ".join(part for part in parts if part).strip()

