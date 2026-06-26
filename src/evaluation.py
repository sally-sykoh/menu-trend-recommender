"""Evaluation helpers for a recommendation-system portfolio narrative."""

from __future__ import annotations

import pandas as pd


def precision_at_k(recommended_ids: list[int], relevant_ids: set[int], k: int = 10) -> float:
    """Compute Precision@K when you have manually labeled relevant recipes."""
    if k <= 0:
        return 0.0
    top_k = recommended_ids[:k]
    if not top_k:
        return 0.0
    return sum(recipe_id in relevant_ids for recipe_id in top_k) / len(top_k)


def coverage(recommendations: pd.DataFrame, catalog_size: int) -> float:
    """Share of catalog represented in recommendation results."""
    if catalog_size <= 0 or recommendations.empty:
        return 0.0
    return recommendations["recipe_id"].nunique() / catalog_size


def score_distribution(recommendations: pd.DataFrame) -> pd.Series:
    """Summarize recommendation score spread for monitoring."""
    if "final_score" not in recommendations:
        return pd.Series(dtype=float)
    return recommendations["final_score"].describe()

