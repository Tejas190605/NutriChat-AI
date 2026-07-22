# Changelog (CHANGELOG.md)

All notable changes to the NutriChat AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

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
