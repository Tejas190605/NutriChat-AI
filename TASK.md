# Master Project Task Tracker (TASK.md)

This checklist tracks the execution milestones for NutriChat AI development.

---

## Epic 1: Workspace Initialization (Complete)
### Milestone 1.1: Environment Bootstrap
*   **Phase**: Bootstrap
*   **Task ID**: `TASK-001`
*   **Description**: Create 20 workspace configuration, organization, workflow, and tracking files.
*   **Priority**: High
*   **Dependencies**: None
*   **Estimated Effort**: 4 hours
*   **Status**: Completed
*   **Owner Agent**: Technical Writer
*   **Completion Checklist**:
    *   [x] Create AGENTS.md
    *   [x] Create SKILLS.md
    *   [x] Create RULES.md
    *   [x] Create WORKFLOWS.md
    *   [x] Create TASK.md
    *   [x] Create PROGRESS.md
    *   [x] Create DECISIONS.md
    *   [x] Create CHANGELOG.md
    *   [x] Rewrite README.md
    *   [x] Create CONTRIBUTING.md
    *   [x] Create CODE_OF_CONDUCT.md
    *   [x] Create SECURITY.md
    *   [x] Create ARCHITECTURE.md
    *   [x] Create API_REFERENCE.md
    *   [x] Create TESTING.md
    *   [x] Create DEPLOYMENT.md
    *   [x] Create ROADMAP.md
    *   [x] Create RISK_REGISTER.md
    *   [x] Create KNOWN_ISSUES.md
    *   [x] Create STYLE_GUIDE.md

---

## Epic 2: Backend Core Infrastructure
### Milestone 2.1: FastAPI Setup & Database Configuration
*   **Phase**: Backend Phase 1
*   **Task ID**: `TASK-002`
*   **Description**: Setup FastAPI app boilerplate, database connection configuration, and migration pathways.
*   **Priority**: High
*   **Dependencies**: `TASK-001`
*   **Estimated Effort**: 6 hours
*   **Status**: Completed
*   **Owner Agent**: FastAPI Engineer
*   **Completion Checklist**:
    *   [x] Create boilerplate directories (`backend/`, `tests/`)
    *   [x] Configure SQLAlchemy engine, session maker, base model
    *   [x] Configure Alembic migrations setup
    *   [x] Write API health routes
    *   [x] Add database connectivity checks in health endpoint

### Milestone 2.2: User Management & Authentication
*   **Phase**: Backend Phase 1
*   **Task ID**: `TASK-003`
*   **Description**: Implement database schemas, auth routines, and JWT protection.
*   **Priority**: High
*   **Dependencies**: `TASK-002`
*   **Estimated Effort**: 8 hours
*   **Status**: Todo
*   **Owner Agent**: Authentication Engineer
*   **Completion Checklist**:
    *   [ ] Create User entity database schema
    *   [ ] Write password hashing utility functions
    *   [ ] Implement `/api/v1/auth/register` route
    *   [ ] Implement `/api/v1/auth/login` route returning JWT
    *   [ ] Write route auth dependency validation checks

---

## Epic 3: AI Pipeline & Integrations
### Milestone 3.1: Multimodal Intake Webhook
*   **Phase**: AI Phase 1
*   **Task ID**: `TASK-004`
*   **Description**: Setup WhatsApp Cloud API webhook endpoint to accept text, audio, and image payloads.
*   **Priority**: High
*   **Dependencies**: `TASK-002`
*   **Estimated Effort**: 10 hours
*   **Status**: Todo
*   **Owner Agent**: API Engineer
*   **Completion Checklist**:
    *   [ ] Implement `/api/v1/webhook` verify token endpoint
    *   [ ] Setup incoming webhook HMAC SHA-256 validation using `X-Hub-Signature-256` header
    *   [ ] Setup parsing logic for incoming text WhatsApp messages
    *   [ ] Implement `/reset` keyword conversational onboarding reset logic
    *   [ ] Setup parsing logic for WhatsApp image URLs
    *   [ ] Integrate Redis cache for incoming message deduplication
    *   [ ] Mock WhatsApp sending response module

### Milestone 3.2: Food Recognition & Nutrition Parsing
*   **Phase**: AI Phase 1
*   **Task ID**: `TASK-005`
*   **Description**: Connect Gemini/GPT-4 Vision models, OCR engines, and Edamam APIs.
*   **Priority**: High
*   **Dependencies**: `TASK-004`
*   **Estimated Effort**: 12 hours
*   **Status**: Todo
*   **Owner Agent**: Computer Vision Engineer
*   **Completion Checklist**:
    *   [ ] Write Vision API wrapper client
    *   [ ] Code Indian Food dish classifier instructions
    *   [ ] Implement serving portion estimation logic
    *   [ ] Setup Edamam REST client for ingredient macros query
    *   [ ] Write barcode matching module using Open Food Facts

### Milestone 3.3: Exercise & Activity Core
*   **Phase**: AI Phase 1
*   **Task ID**: `TASK-008`
*   **Description**: Implement MET-based activity calculations and logging logic.
*   **Priority**: Medium
*   **Dependencies**: `TASK-002`
*   **Estimated Effort**: 8 hours
*   **Status**: Todo
*   **Owner Agent**: ML Engineer
*   **Completion Checklist**:
    *   [ ] Setup user activity database model mappings
    *   [ ] Write MET coefficient matching utility function
    *   [ ] Create `/api/v1/activities/log` endpoint
    *   [ ] Write calorie adjustment pipeline checks

---

## Epic 4: Analytics & Admin Dashboard
### Milestone 4.1: Dashboard UI Scaffold
*   **Phase**: Frontend Phase 1
*   **Task ID**: `TASK-006`
*   **Description**: Initialize Next.js dashboard project with UI layout.
*   **Priority**: Medium
*   **Dependencies**: `TASK-001`
*   **Estimated Effort**: 8 hours
*   **Status**: Todo
*   **Owner Agent**: NextJS Engineer
*   **Completion Checklist**:
    *   [ ] Run NextJS App scaffolding
    *   [ ] Setup Tailwind configuration, style system
    *   [ ] Create layout component panels (Sidebar, TopBar)
    *   [ ] Style main statistics page grid structures

### Milestone 4.2: Data Integration & Reporting Charts
*   **Phase**: Frontend Phase 1
*   **Task ID**: `TASK-007`
*   **Description**: Fetch real-time DB metrics from backend and render charts.
*   **Priority**: Medium
*   **Dependencies**: `TASK-006`, `TASK-003`
*   **Estimated Effort**: 10 hours
*   **Status**: Todo
*   **Owner Agent**: React Engineer
*   **Completion Checklist**:
    *   [ ] Implement analytics backend charts route
    *   [ ] Design line charts for daily/weekly active users count
    *   [ ] Write user calorie goal progress meters components
    *   [ ] Setup automated database logs audit view
