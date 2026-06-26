"""Semantic similarity scoring with sentence-transformers fallback."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.trend_expansion import build_expanded_query


DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"


def compute_semantic_similarity(
    df: pd.DataFrame,
    query: str,
    text_column: str = "recipe_text",
    model_name: str = DEFAULT_MODEL_NAME,
) -> pd.Series:
    """Compute query-to-recipe similarity.

    The preferred path uses sentence-transformers. If the model is not installed
    or cannot be downloaded, the function falls back to TF-IDF so the MVP remains
    usable in restricted local environments.
    """
    texts = df[text_column].fillna("").astype(str).tolist()
    expanded_query = build_expanded_query(query)

    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(model_name)
        recipe_embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        query_embedding = model.encode([expanded_query], normalize_embeddings=True)
        scores = np.asarray(query_embedding).dot(np.asarray(recipe_embeddings).T).ravel()
    except Exception:
        scores = _fallback_text_similarity(expanded_query, texts)

    scores = np.clip(scores, 0, 1)
    return pd.Series(scores, index=df.index, name="semantic_similarity")


def _fallback_text_similarity(query: str, texts: list[str]) -> np.ndarray:
    """Use TF-IDF if sklearn exists, otherwise a simple token-overlap fallback."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform([query, *texts])
        return cosine_similarity(matrix[0:1], matrix[1:]).ravel()
    except Exception:
        query_tokens = _tokenize(query)
        scores = []
        for text in texts:
            text_tokens = _tokenize(text)
            if not query_tokens or not text_tokens:
                scores.append(0.0)
                continue
            scores.append(len(query_tokens & text_tokens) / len(query_tokens | text_tokens))
        return np.array(scores)


def _tokenize(text: str) -> set[str]:
    """Very small fallback tokenizer used only when ML packages are unavailable."""
    return {token for token in text.lower().replace("-", " ").split() if len(token) > 2}
