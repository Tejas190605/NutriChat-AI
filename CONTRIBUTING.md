# Contributing Guidelines (CONTRIBUTING.md)

Welcome to the NutriChat AI project! We are excited to have you contribute. Please follow these guidelines to make the process smooth and productive.

---

## 1. Governance & Rules
Before writing code, make sure you are familiar with:
*   [RULES.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/RULES.md) (Permanent Development Constraints).
*   [STYLE_GUIDE.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/STYLE_GUIDE.md) (Code style and conventions).
*   [CODE_OF_CONDUCT.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/CODE_OF_CONDUCT.md) (Community standards).

---

## 2. Getting Started
1.  **Fork the Repository**: Clone your fork locally.
2.  **Scaffold Dependencies**:
    *   Backend: Install dependencies using `pip install -r backend/requirements.txt`.
    *   Frontend: Install dependencies using `npm install` inside the `frontend/` folder.
3.  **Create a Branch**: Use names like `feat/feature-name` or `fix/bug-name`.

---

## 3. Writing Code & Commit Quality
*   Keep your code changes focused. Do not mix unrelated refactors in a feature branch.
*   Write automated test suites. Make sure to run tests locally using `pytest`.
*   Format code (Black/Ruff) and check typing rules (`mypy`) before staging changes.
*   Write clear commit messages:
    *   *Good*: `feat: add user registration endpoint`
    *   *Bad*: `fix: bugs`

---

## 4. Submitting a Pull Request
1.  Push your changes to your fork.
2.  Open a Pull Request (PR) against our `main` branch.
3.  Describe your changes in detail, link related issues, and attach snapshots of verification runs.
4.  Ensure that CI check pipelines pass successfully.
