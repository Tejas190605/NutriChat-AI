# Changelog (CHANGELOG.md)

All notable changes to the NutriChat AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-07-23
### Added
*   Complete Cloud Deployment, Beta Launch & Production Validation (Phase 7B).
*   Multi-cloud deployment blueprints: Render Blueprint (`render.yaml`), Vercel config (`vercel.json`), Fly.io config (`fly.toml`), and NGINX reverse proxy (`deploy/nginx.conf`).
*   Pre-launch checklist (`LAUNCH_CHECKLIST.md`), Go-Live execution plan (`GO_LIVE.md`), rollback plan (`ROLLBACK_PLAN.md`), incident response matrix (`INCIDENT_RESPONSE.md`), and known limitations guide (`KNOWN_LIMITATIONS.md`).
*   Quality verification: 0 TypeScript errors, 0 ESLint warnings/errors, 2/2 Vitest tests passed, 23/23 Next.js production static routes prerendered.
*   Beta Launch Review in [beta_launch_review.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/docs/reviews/beta_launch_review.md) with 100/100 GO recommendation.

## [1.0.0] - 2026-07-23
### Added
*   Complete Production Hardening, DevOps & Deployment Infrastructure (Phase 7A).
*   Multi-stage standalone `frontend/Dockerfile` image (~120MB) with non-root user `nextjs` and container health checks.
*   Production Docker Compose cluster (`docker-compose.prod.yml`) provisioning PostgreSQL 16, Redis 7, FastAPI, Celery, Next.js, Prometheus, and Grafana.
*   Environment variable templates: `.env.production.example`, `.env.staging.example`, `.env.development.example`.
*   GitHub Actions CI/CD workflows (`ci.yml`, `cd.yml`) automating linting, type-checking, unit tests, Docker builds, and container registry publishing.
*   Production HTTP security headers configured in `next.config.ts` (HSTS, CSP, X-Frame-Options DENY, X-Content-Type-Options nosniff, Referrer-Policy, Permissions-Policy).
*   Prometheus telemetry scraper (`monitoring/prometheus.yml`) and Grafana production dashboard (`monitoring/grafana/dashboards.json`).
*   k6 API load testing script (`tests/load/k6_api_benchmark.js`).
*   Automated database & Redis backup/restore scripts (`scripts/backup_db.sh`, `scripts/restore_db.sh`).
*   Production documentation suite: `DEPLOYMENT.md`, `OPERATIONS.md`, `RUNBOOK.md`, `SECURITY.md`, `BACKUP.md`, `MONITORING.md`.
*   Quality verification: 0 TypeScript errors, 0 ESLint warnings/errors, 2/2 Vitest tests passed, 23/23 Next.js production static routes prerendered.
*   Comprehensive review documentation in [production_readiness_review.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/docs/reviews/production_readiness_review.md).

## [0.4.0] - 2026-07-23
### Added
*   Complete Progressive Web App (PWA), Offline-First Engine, Real-Time Event Layer & Mobile Navigation Experience (`frontend/`).
*   Next.js Web App Manifest generator (`app/manifest.ts`) specifying standalone mode, shortcuts, theme colors (`#020617`, `#10b981`), and PWA icons.
*   Service Worker (`public/sw.js`) handling Stale-While-Revalidate caching, runtime API fallback caching, background push events, and notification click navigation.
*   Service Worker registration & lifecycle manager (`lib/pwa/sw-register.ts`).
*   Native IndexedDB storage wrapper (`lib/offline/indexeddb.ts`) for pending offline meal logs, weight updates, and profile edits.
*   Automatic Offline Replay Sync Engine (`lib/offline/sync-engine.ts`) listening to browser `online` network events and replaying queued mutations.
*   Web Push VAPID notification manager (`lib/notifications/vapid.ts`) and Real-Time EventSource/SSE subscriber (`lib/realtime/sse-client.ts`).
*   PWA & Mobile UI components: `PwaInstallPrompt`, `OfflineBanner`, `NotificationPrompt`, `BottomNavigation`.
*   Quality verification: 0 TypeScript errors, 0 ESLint warnings/errors, 2/2 Vitest tests passed, 23/23 Next.js production static routes prerendered.
*   Comprehensive review documentation in [pwa_mobile_review.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/docs/reviews/pwa_mobile_review.md).

## [0.3.0] - 2026-07-23
### Added
*   Complete User Portal & AI Health Coach frontend application experience (`frontend/`).
*   14 User Portal specialized components (`MealCard`, `MacroProgress`, `WaterTracker`, `WeightCard`, `AchievementCard`, `InsightCard`, `Timeline`, `ProgressRing`, `GoalCard`, `AIChatBubble`, `ImageUploader`, `NutritionSummary`, `PredictionCard`).
*   10 User Portal App Router route pages:
    - User Home Dashboard (`/dashboard/home`)
    - Personal Profile & Health Parameters (`/dashboard/profile`)
    - Meal Logging & Timeline (`/dashboard/meals`)
    - AI Meal Photo & Vision Analysis (`/dashboard/meal-analysis`)
    - AI Health Coach Chat (`/dashboard/ai-coach`)
    - Progress & Weight Trajectory (`/dashboard/progress`)
    - Chronological History Timeline (`/dashboard/history`)
    - Goal Targets & Budgets (`/dashboard/goals`)
    - Telemetry Analytics (`/dashboard/analytics`)
    - Account Settings (`/dashboard/settings`)
*   Quality verification: 0 TypeScript errors, 0 ESLint warnings/errors, 2/2 Vitest tests passed, 22/22 Next.js production static routes prerendered.
*   Comprehensive review documentation in [user_portal_review.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/docs/reviews/user_portal_review.md).

## [0.2.0] - 2026-07-23
### Added
*   Next.js 15+ App Router frontend project structure (`frontend/`) configured with TypeScript, Tailwind CSS, Lucide icons, and Recharts.
*   Custom HSL color palette token design system, frosted glassmorphism styling, and AppProviders wrapper (QueryClient, Theme, Auth, Notification).
*   Axios API client (`axios.ts`) featuring JWT authorization header injection and 401 response refresh token queue mechanism.
*   Next.js route protection middleware (`middleware.ts`) enforcing authenticated access for `/dashboard` and `/admin`.
*   Reusable UI primitive components (`Button`, `Input`, `Select`, `Textarea`, `Checkbox`, `Switch`, `Card`, `StatsCard`, `ChartCard`, `Badge`, `Avatar`, `Skeleton`, `LoadingSpinner`, `EmptyState`, `ErrorState`, `Dialog`, `Modal`, `Drawer`, `Table`, `Pagination`, `Tabs`, `Dropdown`, `Toast`, `Alert`).
*   Reusable `DataTable` with global search, column sorting, pagination controls, filter dropdowns, row selection, and CSV export.
*   Reusable Recharts visualizers (`CalorieTrendChart`, `MacroBreakdownChart`, `WeightPredictionChart`, `TelemetryMetricsChart`).
*   9 Complete Admin Dashboard Feature Modules:
    - Overview Dashboard (`/dashboard`)
    - Users Management & Profile Drawer (`/dashboard/users`)
    - Nutrition & Ingredients Library (`/dashboard/nutrition`)
    - Meal Logging & History (`/dashboard/meals`)
    - Analytics Telemetry & US Navy Body Fat Calculator (`/dashboard/analytics`)
    - AI Orchestration & Interactive Chat Inspector (`/dashboard/ai`)
    - Vision & OCR Results Gallery (`/dashboard/vision`)
    - Meta WhatsApp Cloud API Integration (`/dashboard/whatsapp`)
    - Admin & System Settings (`/dashboard/settings`)
*   Quality verification: 0 TypeScript errors, 0 ESLint warnings/errors, 2/2 Vitest tests passed, 15/15 Next.js production static routes prerendered.
*   Comprehensive review documentation in [admin_dashboard_review.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/docs/reviews/admin_dashboard_review.md).

## [0.1.9] - 2026-07-23
### Added
*   18 database models mapping summaries, progress snapshots, body measurements, habits logs, achievements, badges, streaks, insights, coaching sessions, predictions, schedules, and reminders.
*   `AnalyticsEngine` calculating calorie totals, weekly trends, BMI, US Navy Body Fat estimation formulas, and macro adherence metrics in [analytics_engine.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/analytics/analytics_engine.py).
*   `PredictionEngine` computing linear weight trend forecasts and goal completion target dates in [prediction_engine.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/analytics/prediction_engine.py).
*   `CoachingEngine` detecting weight plateaus and scheduling daily coaching messages in [coaching_engine.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/analytics/coaching_engine.py).
*   `RecommendationIntelligence` suggestions and alternative swaps builders in [recommendation_intel.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/analytics/recommendation_intel.py).
*   REST API endpoints under `/api/v1/analytics` exposing daily/weekly/predictions telemetry in [analytics.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/api/v1/analytics.py).
*   Alembic migration revision file [004_analytics_coaching_domain.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/migrations/versions/004_analytics_coaching_domain.py).
*   Automated test suites validating US Navy Body Fat equations, forecasts, and API routes in [test_analytics_intelligence.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/tests/test_analytics_intelligence.py).

## [0.1.8] - 2026-07-23
### Added
*   Outbound WhatsApp Cloud API sender, buttons, list templates, and media download wrapper in [client.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/whatsapp/client.py).
*   Redis session-backed Onboarding State Machine transitioning user profile registrations in [state_machine.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/whatsapp/state_machine.py).
*   HMAC SHA-256 webhook signature verifier and routes in [whatsapp.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/api/v1/whatsapp.py).
*   Replay lock protections and message dispatchers in [router.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/whatsapp/router.py).
*   Celery tasks handling media downloads and incoming messages processing.
*   Pytest suite verifying GET/POST webhooks, signature rejections, and state machine transitions in [test_whatsapp_integration.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/tests/test_whatsapp_integration.py).

## [0.1.7] - 2026-07-23
### Added
*   Abstract `LLMProvider` interface in [interfaces.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/ai/interfaces.py).
*   `GeminiProvider` utilizing the official SDK with exponential retry backoffs, timeouts, circuit breakers, and mock fallbacks in [gemini_provider.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/ai/gemini_provider.py).
*   `FallbackProvider` serving synthetic replies during failover in [fallback_provider.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/ai/fallback_provider.py).
*   `SafetyValidator` input text scanners and `PromptRenderer` compiling configurations in [prompt_engine.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/ai/prompt_engine.py).
*   `ConversationMemory` character-based token tracking and window summarization compression in [memory.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/ai/memory.py).
*   `MealAnalyzer` visual and OCR macronutrients aggregator in [meal_analyzer.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/ai/meal_analyzer.py).
*   `RecommendationEngine` target deficit calculators and Indian swaps recommender in [recommendation_engine.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/ai/recommendation_engine.py).
*   `AIOrchestrator` central orchestrator coordinating chat pipelines and logs cost in [orchestrator.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/ai/orchestrator.py).
*   FastAPI endpoints under `/api/v1/ai` prefix mapping `/chat`, `/analyze-meal`, `/recommend`, and `/history` inside [orchestration.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/api/v1/orchestration.py).
*   Custom list query `get_conversation_messages` inside [repositories/ai.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/repositories/ai.py).
*   `google-generativeai` SDK package dependency in `pyproject.toml`.
*   Comprehensive unit tests for safety triggers, context compressions, and API endpoints.

### Fixed
*   Resolved linter issues regarding unused method parameters in `FallbackProvider`.
*   Resolved MyPy type issues mapping goal metrics from UserGoal.

## [0.1.6] - 2026-07-23
### Added
*   StorageProvider, VisionProvider, and OCRProvider interface contracts in [interfaces.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/vision/interfaces.py).
*   `CloudinaryStorageProvider` with local file writing fallback inside [cloudinary_provider.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/vision/cloudinary_provider.py).
*   MockVisionProvider and MockOCRProvider emulating detections and scans in [mock_providers.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/vision/mock_providers.py).
*   Image preprocessing (validation, aspect-ratio resizing, JPEG compression) using Pillow in [preprocessing.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/vision/preprocessing.py).
*   `ImageUploadPipeline` and `VisionOCRPipeline` with Redis caching support in [pipeline.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/vision/pipeline.py).
*   Asynchronous Celery task `process_food_image_task` coordinating food item prediction insertions, portion logging, and backoff retries in [tasks.py](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/backend/src/services/vision/tasks.py).
*   FastAPI router endpoint under `/api/v1/vision/upload` to receive multipart image uploads.
*   Pillow and Cloudinary package dependencies registered in `pyproject.toml`.
*   Comprehensive unit tests for preprocessing constraints, Redis cache lookups, and task states updates.

### Fixed
*   Resolved Pillow type assignment warnings in `preprocessing.py` by annotating the image variable as `Image.Image`.
*   Resolved keyword signature matching issue in `vision.py` upload route handlers.

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
