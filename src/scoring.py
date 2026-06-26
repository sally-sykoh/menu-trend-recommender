"""Ranking and score explanation logic."""

from __future__ import annotations

import pandas as pd

from src.trend_expansion import expand_trend_query


DEFAULT_WEIGHTS = {
    "semantic_similarity": 0.35,
    "ingredient_overlap": 0.25,
    "popularity_score": 0.15,
    "cost_efficiency_score": 0.10,
    "prep_efficiency_score": 0.10,
    "margin_score": 0.05,
}


def compute_ingredient_overlap(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Score overlap between trend ingredients and each recipe's ingredients."""
    expansion = expand_trend_query(query)
    trend_ingredients = set(expansion["ingredients"])
    scored = df.copy()

    if not trend_ingredients:
        scored["matched_ingredients"] = [[] for _ in range(len(scored))]
        scored["ingredient_overlap"] = 0.0
        return scored

    def find_matches(recipe_ingredients: list[str]) -> list[str]:
        matches = []
        for trend_ingredient in trend_ingredients:
            for recipe_ingredient in recipe_ingredients:
                if trend_ingredient in recipe_ingredient or recipe_ingredient in trend_ingredient:
                    matches.append(trend_ingredient)
                    break
        return sorted(set(matches))

    scored["matched_ingredients"] = scored["clean_ingredients"].apply(find_matches)
    scored["ingredient_overlap"] = scored["matched_ingredients"].apply(
        lambda matches: len(matches) / max(len(trend_ingredients), 1)
    )
    return scored


def compute_final_score(
    df: pd.DataFrame,
    weights: dict[str, float] | None = None,
) -> pd.DataFrame:
    """Combine normalized feature scores into the weighted final rank."""
    weights = weights or DEFAULT_WEIGHTS
    scored = df.copy()
    scored["final_score"] = 0.0
    for column, weight in weights.items():
        if column not in scored.columns:
            scored[column] = 0.5
        scored["final_score"] += weight * scored[column].fillna(0.5)
    return scored


def build_explanation(row: pd.Series) -> str:
    """Generate a short business-facing recommendation explanation."""
    reasons = []
    if row.get("semantic_similarity", 0) >= 0.45:
        reasons.append("strong semantic match to the trend")
    if row.get("matched_ingredients"):
        reasons.append("uses trend-relevant ingredients: " + ", ".join(row["matched_ingredients"][:5]))
    if row.get("popularity_score", 0) >= 0.65:
        reasons.append("has strong popularity signals")
    if row.get("prep_efficiency_score", 0) >= 0.65:
        reasons.append("is operationally quick to prepare")
    if row.get("cost_efficiency_score", 0) >= 0.65:
        reasons.append("looks cost efficient")
    if row.get("margin_score", 0) >= 0.65:
        reasons.append("has attractive margin potential")

    if not reasons:
        reasons.append("has a balanced score across similarity and business features")
    return "Recommended because it " + "; ".join(reasons) + "."

