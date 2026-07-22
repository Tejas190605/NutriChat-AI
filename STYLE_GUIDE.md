# Coding Style Guide (STYLE_GUIDE.md)

This guide defines the syntax standards, naming conventions, docstring styles, and folder rules for Python and React/NextJS components in NutriChat AI.

---

## 1. Python Style Guide (FastAPI Backend)

### Code Formatting
*   Follow **PEP 8** coding conventions.
*   Line length limit: **88 characters** (standard Black formatter setting).
*   Use standard Black or Ruff code formatter before staging commits.

### Naming Conventions
*   **Modules & Packages**: `snake_case` (e.g. `user_routes.py`).
*   **Classes**: `PascalCase` (e.g. `DatabaseSessionManager`).
*   **Functions & Methods**: `snake_case` (e.g. `get_user_profile`).
*   **Variables**: `snake_case` (e.g. `meal_calories`).
*   **Constants**: `UPPER_SNAKE_CASE` (e.g. `MAX_MEALS_PER_DAY`).

### Docstring Standards
Use Google-style docstrings:
```python
def calculate_macros(food_name: str, quantity: float) -> dict:
    """Calculates macro metrics for a given food keyword.

    Args:
        food_name: The name or query string for the food item.
        quantity: The quantity of the food (e.g. weight in grams).

    Returns:
        A dictionary containing calorie, protein, fat, and carb mappings.
    """
    pass
```

---

## 2. Typescript & React Style Guide (Frontend Dashboard)

### Naming Conventions
*   **Components & Page Layouts**: `PascalCase` (e.g. `UserCalorieChart.tsx`).
*   **Hooks & Utilities**: `camelCase` (e.g. `useFetchAnalytics.ts`).
*   **Style Classes**: Use Tailwind utility sequences ordered cleanly.

---

## 3. Directory Layout Rules
Every new source file must match the established directories:
*   FastAPI API endpoint routes reside in `backend/routes/`.
*   Database models reside in `backend/models/`.
*   Helper integrations (e.g. Edamam, WhatsApp Cloud API) reside in `backend/services/`.
*   Prompt files reside in `backend/prompts/` or `backend/ai/`.
