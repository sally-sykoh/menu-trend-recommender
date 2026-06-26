# Trend-to-Menu Intelligence System

AI-assisted decision support MVP for menu planning and recipe adaptation.

This project was inspired by a product discussion about how restaurant brands can use AI in menu development. The key insight was that AI should not fully create new menus by itself. Instead, it should help teams detect food trends earlier, connect those trends to internal recipe assets, and provide evidence for faster menu planning decisions.

In this MVP, the system takes a food trend keyword or natural-language business question and recommends existing recipes that could be reused or adapted into trend-driven menu ideas.

Example question:

```text
Pizza is trending. Which existing recipes in our database could be reused or adapted into pizza-related menu items?
```

## Problem

Menu development in restaurant brands often depends on manual trend research, individual experience, and scattered internal data. This can create several issues:

- Trends may be discovered too late.
- Similar internal recipes may already exist but remain hard to find.
- Menu planning, R&D, cost review, and marketing are often disconnected.
- Teams spend time collecting and organizing information instead of making decisions.
- Launch timing can matter as much as the menu idea itself.

This project frames the problem as a ranking and decision-support task:

```text
Given a food trend signal, which existing recipes are most adaptable, operationally feasible, and business-relevant?
```

## Current MVP Scope

The current MVP focuses on the core recommendation problem: connecting a user-entered trend query with existing recipe assets.

Implemented features:

- Recipe dataset loading with flexible column mapping.
- Recipe text preprocessing for names, ingredients, tags, and instructions.
- Recipe-level feature engineering.
- Trend keyword expansion with related concepts and ingredients.
- Semantic similarity between trend query and recipe text.
- Ingredient overlap scoring between trend-related ingredients and recipe ingredients.
- Business-feasibility scoring using popularity, prep efficiency, cost efficiency, and margin signals.
- Final weighted recommendation ranking.
- Score breakdown and explanation for each recommended recipe.
- Streamlit dashboard for interactive exploration.

This MVP is intentionally not a fully autonomous menu creator. It is designed to support human menu planners by surfacing relevant candidates and explaining why they may be worth reviewing.

## Recommendation Score

```text
final_score =
0.35 * semantic_similarity
+ 0.25 * ingredient_overlap
+ 0.15 * popularity_score
+ 0.10 * cost_efficiency
+ 0.10 * prep_efficiency
+ 0.05 * margin_score
```

Score components:

- `semantic_similarity`: how closely the recipe text matches the trend query.
- `ingredient_overlap`: how many trend-related ingredients appear in the recipe.
- `popularity_score`: rating and review-count based popularity signal.
- `cost_efficiency_score`: higher score for lower-cost recipes when cost data exists.
- `prep_efficiency_score`: higher score for faster recipes.
- `margin_score`: higher score for higher-margin recipes when margin data exists.

If `cost` or `margin` is missing, the MVP uses a neutral placeholder score of `0.5`. This keeps the ranking pipeline stable while making it clear where real internal business data would improve the model.

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

## Dataset

Place a recipe CSV file at:

```text
data/raw/recipes.csv
```

The code is designed to work with Kaggle-style recipe datasets such as Food.com Recipes, Food.com Recipes and Interactions, Food.com Recipes and Reviews, or Epicurious recipes.

Expected or mappable columns:

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
- optional: `cost`
- optional: `margin`
- optional: `cuisine`
- optional: `diet`

If the dataset uses different column names, update `DEFAULT_COLUMN_MAP` in `src/data_loader.py`.

If no CSV is available, the app uses a small built-in sample dataset so the MVP can still run.

## How to Run Locally

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

## Portfolio Positioning

This project is best described as a data science and recommendation-system MVP, not as a chatbot.

Resume-friendly summary:

```text
Built a Streamlit-based recommendation system that connects food trend queries to reusable internal recipes using sentence embeddings, ingredient overlap, and business-feasibility scoring to support menu planning decisions.
```

Key data science elements:

- Feature engineering from recipe metadata, ingredients, ratings, review counts, prep time, cost, and margin.
- Semantic retrieval using sentence-transformer embeddings with fallback similarity logic.
- Ingredient-level overlap scoring.
- Weighted ranking model.
- Explainable recommendation output.
- Evaluation-ready structure with Precision@K and coverage helpers.

## Future Production Extensions

The broader business idea can be extended into a menu intelligence system by connecting additional data sources and workflows. These are not implemented in the current MVP; they are production roadmap items.

- External trend sensing from Google Trends, TikTok, YouTube, communities, news, delivery apps, and competitor menus.
- POS and sales data integration for brand-level sales, margin, seasonality, and historical menu performance analysis.
- Large-scale recipe catalog search using SQLite, DuckDB, BigQuery, or another analytics database.
- Adaptation classification such as `Ready to Adapt`, `Minor Modification Needed`, and `New Development Needed`.
- Margin-aware menu portfolio analysis using food cost, expected price, and sales mix.
- Marketing channel suggestions based on where each trend is emerging.
- Influencer or content-angle suggestions for launch planning.
- Automated weekly trend and menu opportunity reports for planning meetings.
- Experiment tracking, model cards, and human-labeled validation sets for ranking evaluation.

## 한국어 요약

이 프로젝트는 외식 브랜드의 메뉴 기획을 돕는 AI 의사결정 보조 MVP입니다.

핵심 아이디어는 AI가 신메뉴를 직접 완성하는 것이 아니라, 외부 트렌드와 내부 레시피 자산을 연결해 사람이 더 빠르고 근거 있는 메뉴 기획 결정을 할 수 있도록 돕는 것입니다.

현재 MVP는 사용자가 입력한 음식 트렌드 키워드나 질문을 기존 레시피 데이터와 비교해, 재활용하거나 변형할 가능성이 높은 레시피 후보를 추천합니다.

예시 질문:

```text
피자가 트렌드입니다. 기존 레시피 중 피자 관련 메뉴로 재활용하거나 변형할 수 있는 레시피는 무엇인가요?
```

## 현재 구현 범위

- 레시피 데이터 로딩 및 컬럼 매핑
- 재료, 태그, 조리 방법, 레시피명 전처리
- 레시피 단위 feature engineering
- 트렌드 키워드 확장
- 트렌드 질문과 레시피 텍스트 간 semantic similarity 계산
- 트렌드 관련 재료와 레시피 재료 간 ingredient overlap 계산
- 인기도, 조리 효율, 비용 효율, 마진 가능성을 반영한 비즈니스 점수 계산
- 최종 weighted recommendation ranking
- 추천 결과별 점수 breakdown과 추천 이유 제공
- Streamlit dashboard 구현

이 프로젝트는 AI가 메뉴를 자동으로 만들어주는 시스템이 아니라, 메뉴 기획자가 검토할 후보를 빠르게 찾고 판단 근거를 확인할 수 있도록 돕는 의사결정 보조 시스템입니다.

## 실무 확장 방향

회의에서 논의된 원래 아이디어는 아래와 같은 방향으로 확장할 수 있습니다. 아래 항목들은 현재 MVP에 모두 구현된 기능이 아니라, 실무 적용 시 확장 가능한 로드맵입니다.

- Google Trends, TikTok, YouTube, 커뮤니티, 뉴스, 배달앱 기반 외부 트렌드 센싱
- POS 및 판매 데이터 연동을 통한 브랜드별 판매량, 마진율, 시즌성, 메뉴 성과 분석
- SQLite, DuckDB, BigQuery 기반 대용량 레시피 카탈로그 검색
- `바로 활용 가능`, `일부 수정 필요`, `신규 개발 필요` 같은 메뉴 후보 분류
- 원가, 예상 판매가, 판매 구성비를 반영한 마진 기반 메뉴 포트폴리오 분석
- 트렌드 발생 채널을 기반으로 한 마케팅 채널 및 콘텐츠 방향 제안
- 인플루언서 후보 또는 콘텐츠 angle 제안
- 메뉴 기획 회의용 주간 트렌드/메뉴 기회 리포트 자동 생성
- 추천 모델 실험 관리, 모델 카드, 사람이 검수한 validation set 기반 평가

## 레주메용 한 줄 설명

```text
외식 브랜드의 메뉴 기획을 돕기 위해 음식 트렌드 키워드와 기존 레시피 자산을 연결하는 추천 시스템 MVP를 개발했습니다. 문장 임베딩 기반 의미 유사도, 재료 겹침 점수, 인기도, 조리 효율, 비용 효율, 마진 점수를 결합해 재활용 가능한 메뉴 후보를 랭킹하고 추천 근거를 제공했습니다.
```
