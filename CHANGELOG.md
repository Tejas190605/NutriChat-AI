# Changelog (CHANGELOG.md)

All notable changes to the NutriChat AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.5] - 2026-07-23
### Added
*   14 database models mapping the AI persistence domain (FoodImage, OCRResult, VisionPrediction, AIConversation, AIMessage, PromptTemplate, PromptVersion, AIRequest, AIResponse, Recommendation, RecommendationFeedback, ConfidenceScore, TokenUsage, ModelUsage) in [models/](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/models/).
*   Pydantic validation schemas checking session creation parameters, messages creation parameters, prompts templates creations, recommendation requests, and feedback metrics in [schemas/](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/schemas/).
*   Asynchronous repositories wrapping conversation history retrievals, prompt lookups, and model aggregated analytics cost counters in [repositories/](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/repositories/).
*   AIConversationService, AIPromptService, RecommendationService, VisionPersistenceService, and AIAnalyticsService managing state changes, deactivating duplicate active version configs, logging CV coordinates, and tracking execution latencies.
*   REST endpoint routers under `/api/v1/ai` exposing conversations list/starts/deletes, message history replies, prompts templating versions, and suggestions feedback loggers.
*   Alembic migration revision script [003_ai_persistence_domain.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/migrations/versions/003_ai_persistence_domain.py) managing SQL tables declarations and indexes optimizations.
*   Thorough testing coverage validating active model configurations, token costs, rating feedback logging, and router parameter inputs.

### Fixed
*   Resolved MyPy generic type assignments errors inside `ai_service.py` by compiling standard SQLAlchemy `update` expressions.
*   Resolved MyPy variable type checks inside `ai.py` route controllers by declaring `update_dict` types explicitly as `dict[str, Any]`.

## [0.1.4] - 2026-07-23
### Added
*   13 database models mapping the nutrition domain (Food, FoodCategory, Ingredient, Meal, MealItem, NutritionProfile, NutritionFact, BarcodeProduct, NutritionLabel, RestaurantMenu, GroceryProduct, FavoriteFood, RecentFood) in [models/](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/models/).
*   Pydantic validation schemas for logging meals, retrieving daily summaries vs targets progress, and weekly averages inside [schemas/](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/schemas/).
*   Asynchronous repositories mapping database relations for Food, Category, Favorites, Recents, Meals, and Barcodes in [repositories/](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/repositories/).
*   `MealService` managing logs insertions, portions updates, soft deletes, daily progress vs targets calculation, and weekly averages calculations in [meal_service.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/meal_service.py).
*   `NutritionService` wrapping food text lookups, barcode lookups, and favorites registry lists in [nutrition_service.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/nutrition_service.py).
*   FastAPI endpoint routers under `/api/v1/meals` and `/api/v1/nutrition` registered inside the main application entry point.
*   Alembic migration revision script [002_nutrition_domain.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/migrations/versions/002_nutrition_domain.py) creating schema tables, unique constraints, and search optimizations indexes.
*   Integration and unit test suites covering the services logic and API parameters validation in [tests/](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/tests/).

### Fixed
*   Resolved Ruff `ARG001` unused parameter errors by renaming authentication dependents to `_current_user` in lookup routes.
*   Resolved MyPy generic type warnings by specifying type arguments for dictionary return types in meal service.

## [0.1.3] - 2026-07-22
### Added
*   11 database models mapping the user domain (User, UserProfile, UserGoal, UserPreference, Allergy, DietaryPreference, ActivityLevel, WeightHistory, UserSession, RefreshToken, AuditLog) in [models/](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/models/).
*   Pydantic schemas validating user registration, logins, JWT rotation, profiles, and weight logs in [schemas/](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/schemas/).
*   Generic base repository class and customized async User and RefreshToken queries in [repositories/](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/repositories/).
*   Argon2 credential checks, JWT tokens rotation rules, and active sessions manager in [auth_service.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/auth_service.py).
*   Mifflin-St Jeor TDEE calculators, macro splits splits, profiles completion, and weight history logs in [user_service.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/user_service.py).
*   FastAPI endpoints under `/api/v1/auth` and `/api/v1/users` registered in main API routes.
*   Initial Alembic schema migrations script [001_initial_user_domain.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/migrations/versions/001_initial_user_domain.py).
*   Comprehensive unit, repository, and controller api testing coverage validating user logic with dynamic offline DB skipped fallbacks in [tests/](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/tests/).

### Fixed
*   Refactored deprecated Pydantic v1 `class Config` configurations in schema models to modern `ConfigDict` schemas.
*   Corrected generic base repository models attribute checks using standard properties with selective `# type: ignore[attr-defined]` tags.

## [0.1.2] - 2026-07-22
### Added
*   Production-grade FastAPI project directory structure layout inside `/backend`.
*   Pydantic Settings management class validating critical system environment parameters dynamically in [settings.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/config/settings.py).
*   Structured JSON format logger config in [logging_config.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/core/logging_config.py).
*   SQLAlchemy asynchronous engine pool and base declarative metadata schema registries in [session.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/db/session.py) and [base.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/db/base.py).
*   Redis connection pool helper in [redis_client.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/redis_client.py) and async background task Celery queue setup in [celery_app.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/celery_app.py).
*   Diagnostic API router checks in [health.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/api/health.py) monitoring Postgres/Redis/Celery services health status.
*   Pytest test suite layout verifying root path endpoints and health checks synchronously inside [conftest.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/tests/conftest.py) and [test_health.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/tests/test_health.py).
*   CI scripts including [.pre-commit-config.yaml](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/.pre-commit-config.yaml) and GitHub Actions workflow file [.github/workflows/ci.yml](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/.github/workflows/ci.yml).
*   Multi-stage docker build configuration [Dockerfile](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/Dockerfile) and [docker-compose.yml](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/docker-compose.yml).

### Fixed
*   Migrated synchronous Redis client connections to `redis.asyncio` async client in [redis_client.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/redis_client.py) to prevent event-loop blockages.
*   Refactored [health.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/api/health.py) health endpoint so Celery worker inspection is run in FastAPI's threadpool (`run_in_threadpool`).
*   Hardened [Dockerfile](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/Dockerfile) to create and run as a non-root system user (`appuser`), dropping container root privileges.
*   Replaced wildcard CORS configuration with dynamic settings list `CORS_ORIGINS` parsed natively from JSON arrays in [settings.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/config/settings.py).
*   Cleaned default secrets from [docker-compose.yml](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/docker-compose.yml), migrating database password mappings to environment variable interpolation.

## [0.1.1] - 2026-07-22
### Added
*   Onboarding `/reset` command specifications inside [functional_requirements.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/specs/functional_requirements.md) and state machine configurations inside [ARCHITECTURE.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/ARCHITECTURE.md).
*   HMAC SHA-256 webhook signature security validation check rules for API webhook POST payloads (`X-Hub-Signature-256` header validation).
*   User activity logs tracking schema. Added the `user_activities` table in [schema.sql](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/database/schema.sql) with composite indexing on `(whatsapp_user_id, time DESC)` for database queries optimization.
*   MET coefficient calculations and activity logs tracking routes scheduled subtasks inside [TASK.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/TASK.md).

## [0.1.0] - 2026-07-22
### Added
*   Autonomous AI Organization layout file ([AGENTS.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/AGENTS.md)) defining responsibilities, success criteria, and team escalations.
*   Developer capability checks file ([SKILLS.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/SKILLS.md)) spanning design, APIs, AI processing, and deployment routines.
*   System constraints checklist ([RULES.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/RULES.md)) specifying permanent development guidelines.
*   Autonomous engineering cycles workflow guide ([WORKFLOWS.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/WORKFLOWS.md)).
*   Workspace Epic/Milestone task catalog ([TASK.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/TASK.md)) and progress board ([PROGRESS.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/PROGRESS.md)).
*   ADR database and files setup decisions record ([DECISIONS.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/DECISIONS.md)).
