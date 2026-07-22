# Master Project Task Tracker (TASK.md)

This checklist tracks the execution milestones for NutriChat AI development.

---

## Epic 1: Workspace Initialization (Current)
### Milestone 1.1: Environment Bootstrap
*   **Phase**: Bootstrap
*   **Task ID**: `TASK-001`
*   **Description**: Create 20 workspace configuration, organization, workflow, and tracking files.
*   **Priority**: High
*   **Dependencies**: None
*   **Estimated Effort**: 4 hours
*   **Status**: In Progress
*   **Owner Agent**: Technical Writer
*   **Completion Checklist**:
    *   [x] Create AGENTS.md
    *   [x] Create SKILLS.md
    *   [x] Create RULES.md
    *   [x] Create WORKFLOWS.md
    *   [ ] Create TASK.md
    *   [ ] Create PROGRESS.md
    *   [ ] Create DECISIONS.md
    *   [ ] Create CHANGELOG.md
    *   [ ] Rewrite README.md
    *   [ ] Create CONTRIBUTING.md
    *   [ ] Create CODE_OF_CONDUCT.md
    *   [ ] Create SECURITY.md
    *   [ ] Create ARCHITECTURE.md
    *   [ ] Create API_REFERENCE.md
    *   [ ] Create TESTING.md
    *   [ ] Create DEPLOYMENT.md
    *   [ ] Create ROADMAP.md
    *   [ ] Create RISK_REGISTER.md
    *   [ ] Create KNOWN_ISSUES.md
    *   [ ] Create STYLE_GUIDE.md

---

## Epic 2: Backend Core Infrastructure
### Milestone 2.1: FastAPI Setup & Database Configuration
*   **Phase**: Backend Phase 1
*   **Task ID**: `TASK-002`
*   **Description**: Setup FastAPI app boilerplate, database connection configuration, and migration pathways.
*   **Priority**: High
*   **Dependencies**: `TASK-001`
*   **Estimated Effort**: 6 hours
*   **Status**: Todo
*   **Owner Agent**: FastAPI Engineer
*   **Completion Checklist**:
    *   [ ] Create boilerplate directories (`backend/`, `tests/`)
    *   [ ] Configure SQLAlchemy engine, session maker, base model
    *   [ ] Configure Alembic migrations setup
    *   [ ] Write API health routes
    *   [ ] Add database connectivity checks in health endpoint

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
    *   [ ] Setup parsing logic for incoming text WhatsApp messages
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
