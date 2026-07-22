# Testing Standards & Workflow (TESTING.md)

This document establishes the guidelines, targets, and workflow steps for testing both the backend FastAPI server and the NextJS frontend dashboard of NutriChat AI.

---

## 1. Testing Standards

*   **Test Isolation**: Every test case must run independently. Shared states (such as active databases or session caches) must be refreshed before every test execution.
*   **API Mocks**: External endpoints (Meta WhatsApp Cloud API, Edamam API, Open Food Facts) must not be called during unit/integration tests. Use mock clients and mock responses.
*   **Determinism**: Avoid hardcoding dynamically changing metrics (e.g. current date assertions) without setting explicit timezone limits or mocking time elements.

---

## 2. Coverage Requirements

*   **Overall Code Coverage Target**: Minimum of **85%** total code line coverage.
*   **Critical Paths Requirements**: 100% path coverage for authentication middleware security checks, JWT validations, and webhook payload verifications.
*   **Database Migrations**: Every Alembic migration must have verified downgrade scripts tested locally.

---

## 3. Testing Workflows

### Backend testing (Pytest)
1.  **Configure Test Variables**: Load testing variables from `.env.test`.
2.  **Execute Pytest**: Run the testing suite via:
    ```bash
    pytest --cov=backend tests/
    ```
3.  **Generate Coverage HTML**:
    ```bash
    pytest --cov=backend --cov-report=html tests/
    ```

### Frontend Dashboard Testing
*   **Unit Component Testing**: Write component rendering validations inside `frontend/tests/` using Jest and React Testing Library.
*   **E2E Integration Testing**: Run Cypress or Playwright flow tests:
    ```bash
    cd frontend/
    npm run test:e2e
    ```

---

## 4. CI/CD Integration
Test pipelines run automatically on every pull request submitted to the repository main branch. If any test case fails, code merge actions are locked. Refer to [WORKFLOWS.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/WORKFLOWS.md) for automated execution details.
