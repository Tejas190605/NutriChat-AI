# Permanent Engineering Rules (RULES.md)

This document contains the binding rules and software engineering guidelines for all developers and AI agents working on NutriChat AI.

---

## 1. Code Quality Guidelines
*   **Rule 1.1: No Placeholder Code**
    *   *Directive*: Never submit mock structures, empty function blocks, or dummy returns for active functions. All implementation files must be complete.
*   **Rule 1.2: No TODO Comments**
    *   *Directive*: Do not commit files containing `TODO`, `FIXME`, or `TBD` markers. Address issues immediately or record them formally in [KNOWN_ISSUES.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/KNOWN_ISSUES.md).
*   **Rule 1.3: Absolute Type Safety**
    *   *Directive*: Use Python type annotations everywhere (FastAPI/Pydantic) and TypeScript rules on the NextJS frontend dashboard. No implicit `Any` types.

## 2. Architecture & Design Principles
*   **Rule 2.1: Clean Architecture Separation**
    *   *Directive*: Decouple infrastructure interfaces (FastAPI web routes, database integrations) from internal business entities. Core reasoning logic must stay context-free.
*   **Rule 2.2: SOLID Compliance**
    *   *Directive*: Follow SOLID design principles. Keep classes cohesive (Single Responsibility) and use interfaces to prevent component dependencies from coupling tightly.
*   **Rule 2.3: Dependency Injection**
    *   *Directive*: Always request database sessions, API clients, and settings keys using FastAPI's dependency injection system (`Depends`). Avoid hardcoded config creations.

## 3. Operations & Safety
*   **Rule 3.1: Strict Secrets Management**
    *   *Directive*: Never hardcode API keys, passwords, or salts inside files. All configurations must load from environment variables (`.env` files) validated through Pydantic settings.
*   **Rule 3.2: Robust Input Validation**
    *   *Directive*: Sanitize and validate all incoming inputs (WhatsApp messages, webhook URLs, admin login requests) before execution. Use Pydantic and regex validation libraries.
*   **Rule 3.3: Backward Compatibility**
    *   *Directive*: Keep API responses and database formats backward-compatible to avoid breaking existing users. Version all API changes under `/api/v1/...`.

## 4. Verification & Testing Standards
*   **Rule 4.1: Mandatory Testing**
    *   *Directive*: Every new endpoint or service wrapper must have automated test cases inside the `tests/` directory. Target a test coverage of at least 85%.
*   **Rule 4.2: Automated Auditing & Lints**
    *   *Directive*: Always execute code formatting (Black, Ruff), lint checks (Flake8), and type verifications (MyPy) prior to submitting commits.
*   **Rule 4.3: Implementation Verification**
    *   *Directive*: Run the application locally or in containers to verify behavior before merging branches. Verify API outputs directly.

## 5. Process & Tracking
*   **Rule 5.1: Conventional Commits**
    *   *Directive*: Write informative git commit logs following standard rules (e.g. `feat: implement user onboarding webhook`, `fix: correct Edamam client rate limit backoff`).
*   **Rule 5.2: Sync Task Tracker & Changelog**
    *   *Directive*: On completing any task, update [TASK.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/TASK.md), [PROGRESS.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/PROGRESS.md), and append details to [CHANGELOG.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/CHANGELOG.md) instantly.
*   **Rule 5.3: Documentation Integrity**
    *   *Directive*: Keep code docstrings, API specifications, and setup manuals updated on every structural file modification.
