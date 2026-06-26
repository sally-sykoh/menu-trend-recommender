# AI-Powered Menu Trend Recommendation System

This is a data science portfolio MVP for recommending existing recipes that can be adapted into trend-driven menu ideas.

Example question:

```text
Pizza is trending. Which existing recipes in our database could be reused or adapted into pizza-related menu items?
```

The project is positioned as a recommendation and ranking system, not a chatbot. It uses feature engineering, semantic similarity, ingredient overlap, business scoring, explainability, and a simple Streamlit dashboard.

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

## MVP Features

- Flexible recipe CSV loading with column standardization.
- Beginner-friendly preprocessing for ingredients, tags, instructions, and recipe text.
- Recipe-level feature engineering for popularity, prep efficiency, cost efficiency, and margin.
- Trend keyword expansion dictionary for ingredients and related concepts.
- Semantic similarity using `sentence-transformers`.
- TF-IDF fallback if a transformer model is unavailable in the local environment.
- Ingredient overlap scoring between trend ingredients and recipe ingredients.
- Weighted final recommendation score:

```text
final_score =
0.35 * semantic_similarity
+ 0.25 * ingredient_overlap
+ 0.15 * popularity_score
+ 0.10 * cost_efficiency
+ 0.10 * prep_efficiency
+ 0.05 * margin_score
```

## Dataset

Place your Kaggle recipe CSV at:

```text
data/raw/recipes.csv
```

The code assumes the dataset may contain columns like:

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

If the column names differ, update `DEFAULT_COLUMN_MAP` in `src/data_loader.py`.

If no CSV is available, the app uses a small built-in sample dataset so the MVP still runs.

## Cost and Margin Placeholder Logic

Many public recipe datasets do not include ingredient cost, selling price, or margin. This MVP handles those gaps explicitly:

- If `cost` exists, lower cost receives a higher `cost_efficiency_score`.
- If `cost` is missing, `cost_efficiency_score` defaults to `0.5`, a neutral placeholder.
- If `margin` exists, higher margin receives a higher `margin_score`.
- If `margin` is missing, `margin_score` defaults to `0.5`, a neutral placeholder.

For a production version, cost could be estimated by joining ingredients to supplier prices, and margin could be calculated from expected menu price minus estimated food cost.

## How to Run Locally

From the project folder:

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

## Evaluation Ideas

For a stronger portfolio story, add evaluation in phases:

- Create a manually labeled validation set of trend queries and relevant recipes.
- Measure Precision@K and Recall@K.
- Track score distribution and recommendation diversity.
- Compare ranking variants:
  - semantic-only
  - ingredient-only
  - business-only
  - full weighted model
- Collect qualitative feedback from chefs, menu planners, or product managers.

## Next Improvements

- Add automatic trend extraction from Google Trends, TikTok food trends, or internal sales data.
- Replace static keyword expansion with an LLM-assisted trend-to-ingredient parser.
- Add ingredient substitution suggestions.
- Add SQLite or DuckDB for larger recipe catalogs.
- Add model cards and experiment tracking.

---

# AI 기반 메뉴 트렌드 추천 시스템

이 프로젝트는 음식 트렌드 키워드나 자연어 비즈니스 질문을 입력하면, 기존 레시피 데이터베이스에서 새 메뉴로 재활용하거나 변형할 수 있는 레시피 후보를 추천하는 데이터 사이언스 포트폴리오 MVP입니다.

예시 질문:

```text
피자가 트렌드입니다. 기존 레시피 중 피자 관련 메뉴로 재활용하거나 변형할 수 있는 레시피는 무엇인가요?
```

이 프로젝트는 단순 챗봇이 아니라 추천 시스템과 랭킹 모델 중심으로 설계되었습니다. 레시피 텍스트 임베딩, 재료 매칭, 인기도, 비용 효율, 조리 효율, 마진 점수를 결합해 최종 추천 점수를 계산합니다.

## 프로젝트 구조

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

## 주요 기능

- Kaggle 레시피 CSV 데이터를 불러오고 표준 컬럼명으로 정리합니다.
- 재료, 태그, 조리 방법, 레시피명을 전처리해 검색용 텍스트를 만듭니다.
- 레시피 단위 feature engineering을 수행합니다.
- 트렌드 키워드를 관련 컨셉과 재료로 확장합니다.
- `sentence-transformers`를 사용해 트렌드 질문과 레시피 텍스트 간 의미적 유사도를 계산합니다.
- 로컬 환경에서 transformer 모델을 사용할 수 없으면 TF-IDF 또는 간단한 토큰 유사도 방식으로 fallback합니다.
- 트렌드 관련 재료와 레시피 재료 간 ingredient overlap 점수를 계산합니다.
- 비즈니스 지표를 반영한 최종 추천 점수를 계산합니다.
- Streamlit 대시보드에서 추천 결과, 점수 breakdown, 매칭 재료, 추천 이유를 확인할 수 있습니다.

## 최종 추천 점수

```text
final_score =
0.35 * semantic_similarity
+ 0.25 * ingredient_overlap
+ 0.15 * popularity_score
+ 0.10 * cost_efficiency
+ 0.10 * prep_efficiency
+ 0.05 * margin_score
```

각 점수의 의미:

- `semantic_similarity`: 트렌드 질문과 레시피 텍스트의 의미적 유사도
- `ingredient_overlap`: 트렌드 관련 재료와 레시피 재료의 겹침 정도
- `popularity_score`: 평점과 리뷰 수를 결합한 인기도 점수
- `cost_efficiency_score`: 비용이 낮을수록 높은 점수
- `prep_efficiency_score`: 조리 시간이 짧을수록 높은 점수
- `margin_score`: 마진이 높을수록 높은 점수

## 데이터셋 사용 방법

Kaggle에서 Food.com Recipes, Food.com Recipes and Reviews, Epicurious Recipes 같은 레시피 데이터를 다운로드한 뒤 CSV 파일을 아래 위치에 넣습니다.

```text
data/raw/recipes.csv
```

현재 코드는 다음과 같은 컬럼을 예상합니다.

- `recipe_id`
- `recipe_name`
- `ingredients`
- `tags`
- `steps` 또는 `instructions`
- `minutes` 또는 `prep_time_minutes`
- `nutrition`
- `n_steps`
- `n_ingredients`
- `rating` 또는 `avg_rating`
- `review_count`

실제 데이터셋의 컬럼명이 다르면 `src/data_loader.py`의 `DEFAULT_COLUMN_MAP`을 수정하면 됩니다.

CSV 파일이 없어도 앱은 내장된 작은 샘플 데이터셋으로 실행됩니다. 그래서 Kaggle 데이터를 넣기 전에도 MVP를 바로 테스트할 수 있습니다.

## 비용과 마진 컬럼 처리

공개 레시피 데이터셋에는 원가, 판매가, 마진 정보가 없는 경우가 많습니다. 이 MVP에서는 해당 컬럼이 없을 때 중립 점수인 `0.5`를 사용합니다.

- `cost` 컬럼이 있으면 비용이 낮은 레시피에 더 높은 `cost_efficiency_score`를 부여합니다.
- `cost` 컬럼이 없으면 `cost_efficiency_score = 0.5`로 처리합니다.
- `margin` 컬럼이 있으면 마진이 높은 레시피에 더 높은 `margin_score`를 부여합니다.
- `margin` 컬럼이 없으면 `margin_score = 0.5`로 처리합니다.

실무 버전에서는 재료별 공급 단가 테이블을 연결해 원가를 추정하고, 예상 판매가와 원가를 이용해 마진을 계산할 수 있습니다.

## 로컬 실행 방법

프로젝트 폴더에서 아래 명령어를 실행합니다.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

터미널에 표시되는 Streamlit 로컬 URL을 브라우저에서 열면 됩니다.

## Python에서 직접 사용하기

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

## 포트폴리오에서 강조할 포인트

- 단순 생성형 AI 챗봇이 아니라 데이터 기반 추천 시스템입니다.
- 레시피 단위 feature engineering을 수행합니다.
- semantic similarity와 ingredient overlap을 함께 사용합니다.
- 인기도, 조리 시간, 비용, 마진 같은 비즈니스 신호를 랭킹에 반영합니다.
- 추천 결과마다 점수 breakdown과 설명을 제공합니다.
- 향후 Precision@K, Recall@K, ranking ablation test로 평가를 확장할 수 있습니다.

## 향후 개선 아이디어

- Google Trends, TikTok, 내부 판매 데이터에서 트렌드 키워드 자동 수집
- LLM을 활용한 트렌드 키워드 → 관련 재료 자동 확장
- 레시피별 대체 재료 추천
- SQLite 또는 DuckDB를 활용한 대용량 레시피 카탈로그 관리
- 추천 모델 실험 관리 및 모델 카드 작성
