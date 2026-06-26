"""Trend keyword expansion for ingredient and concept matching."""

from __future__ import annotations

from src.preprocessing import normalize_text


TREND_EXPANSION = {
    "pizza": {
        "concepts": ["flatbread", "pizzeria", "slice", "italian", "baked"],
        "ingredients": [
            "tomato",
            "tomato sauce",
            "mozzarella",
            "cheese",
            "basil",
            "oregano",
            "pepperoni",
            "mushroom",
            "olive oil",
            "dough",
            "flatbread",
        ],
    },
    "taco": {
        "concepts": ["mexican", "street food", "handheld", "tortilla"],
        "ingredients": ["tortilla", "lime", "cilantro", "salsa", "beans", "avocado", "chicken"],
    },
    "korean": {
        "concepts": ["k-food", "spicy", "fermented", "fusion"],
        "ingredients": ["kimchi", "gochujang", "sesame", "scallion", "soy sauce", "garlic"],
    },
    "plant based": {
        "concepts": ["vegan", "vegetarian", "meatless", "healthy"],
        "ingredients": ["tofu", "chickpeas", "lentils", "mushrooms", "cauliflower", "beans"],
    },
    "high protein": {
        "concepts": ["fitness", "protein", "meal prep", "satiety"],
        "ingredients": ["chicken", "egg", "tofu", "beans", "greek yogurt", "tuna", "lentils"],
    },
    "bowl": {
        "concepts": ["grain bowl", "salad bowl", "meal prep", "customizable"],
        "ingredients": ["rice", "quinoa", "greens", "chickpeas", "sauce", "vegetables"],
    },
}


def expand_trend_query(query: str) -> dict[str, list[str]]:
    """Return expanded concepts and ingredients for a trend query."""
    query_norm = normalize_text(query)
    concepts = set()
    ingredients = set()

    for keyword, expansion in TREND_EXPANSION.items():
        if keyword in query_norm:
            concepts.update(expansion["concepts"])
            ingredients.update(expansion["ingredients"])

    # Always include the user's words as concepts so niche trends still work.
    concepts.update(token for token in query_norm.split() if len(token) > 2)

    return {
        "concepts": sorted(concepts),
        "ingredients": sorted(ingredients),
    }


def build_expanded_query(query: str) -> str:
    """Create richer text for semantic embedding."""
    expansion = expand_trend_query(query)
    return " ".join([query, *expansion["concepts"], *expansion["ingredients"]])

