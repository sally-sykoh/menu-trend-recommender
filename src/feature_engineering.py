"""Recipe-level feature engineering for ranking."""

from __future__ import annotations

import numpy as np
import pandas as pd


def safe_numeric(series: pd.Series, default: float | None = None) -> pd.Series:
    """Coerce a column to numeric and fill missing values with a median/default."""
    numeric = pd.to_numeric(series, errors="coerce")
    if default is None:
        default = float(numeric.median()) if numeric.notna().any() else 0.0
    return numeric.fillna(default)


def minmax_score(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Scale a numeric signal into 0-1 for weighted scoring."""
    numeric = safe_numeric(series)
    if numeric.nunique(dropna=False) <= 1:
        return pd.Series(0.5, index=series.index)
    values = (numeric - numeric.min()) / (numeric.max() - numeric.min())
    if not higher_is_better:
        values = 1 - values
    return pd.Series(values, index=series.index)


def add_recipe_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create normalized business features used by the scoring model."""
    featured = df.copy()

    featured["minutes_num"] = safe_numeric(featured["minutes"], default=30.0)
    featured["rating_num"] = safe_numeric(featured["rating"], default=0.0)
    featured["review_count_num"] = safe_numeric(featured["review_count"], default=0.0)
    featured["n_ingredients_num"] = safe_numeric(
        featured["n_ingredients"],
        default=float(featured["clean_ingredients"].apply(len).median() or 1),
    )
    featured["n_steps_num"] = safe_numeric(featured["n_steps"], default=5.0)

    # Popularity blends quality and confidence. log1p prevents review-heavy
    # recipes from completely dominating the rank.
    featured["rating_norm"] = minmax_score(featured["rating_num"])
    featured["review_norm"] = minmax_score(np.log1p(featured["review_count_num"]))
    featured["popularity_score"] = (0.65 * featured["rating_norm"]) + (
        0.35 * featured["review_norm"]
    )

    # Lower cost and lower prep minutes are better for operational adaptation.
    if featured["cost"].notna().any():
        featured["cost_efficiency_score"] = minmax_score(featured["cost"], higher_is_better=False)
    else:
        featured["cost_efficiency_score"] = 0.5

    featured["prep_efficiency_score"] = minmax_score(
        featured["minutes_num"], higher_is_better=False
    )

    if featured["margin"].notna().any():
        featured["margin_score"] = minmax_score(featured["margin"])
    else:
        featured["margin_score"] = 0.5

    return featured
