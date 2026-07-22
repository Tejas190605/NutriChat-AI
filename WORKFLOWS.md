# Autonomous Engineering Workflows (WORKFLOWS.md)

This manual defines the structured workflow protocols that AI agents and developers execute for various stages of the NutriChat AI development cycle.

---

## 1. Research Workflow
*   **Objective**: Gain clarity on third-party APIs, library integrations, or algorithms.
*   **Preconditions**: Unclear requirement or new library integration.
*   **Execution Steps**:
    1.  Locate relevant documentations (e.g. Edamam, WhatsApp Cloud API).
    2.  Write proof-of-concept tests in the `scratch/` folder.
    3.  Analyze limitations, cost tiers, and latency specifications.
*   **Validation**: Verify code returns expected mocks.
*   **Artifacts Produced**: Research notes inside `docs/research/`.
*   **Completion Criteria**: Technical strategy is documented with zero outstanding questions.
*   **Rollback Strategy**: Clean up scratch scripts, return context to current task branches.

## 2. Specification Workflow
*   **Objective**: Define precise requirements and acceptance criteria.
*   **Preconditions**: User request for a new feature.
*   **Execution Steps**:
    1.  Review business goals and targets with the Product Manager.
    2.  Draft functional requirements, edge conditions, and validation limits.
*   **Validation**: Confirm alignment with [PROJECT_SPECIFICATION.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/PROJECT_SPECIFICATION.md).
*   **Artifacts Produced**: Feature specification docs under `docs/features/`.
*   **Completion Criteria**: Acceptance criteria signed off by Product Manager.
*   **Rollback Strategy**: Remove drafts, update status in [PROGRESS.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/PROGRESS.md).

## 3. Architecture Workflow
*   **Objective**: Design structural flow and interfaces.
*   **Preconditions**: Approved feature specification document.
*   **Execution Steps**:
    1.  Draft software modular boundaries.
    2.  Create sequence and block diagrams.
    3.  Perform design patterns assessment.
*   **Validation**: Check against style rules in [STYLE_GUIDE.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/STYLE_GUIDE.md).
*   **Artifacts Produced**: Design updates to [ARCHITECTURE.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/ARCHITECTURE.md).
*   **Completion Criteria**: Technical design approved, schemas defined.
*   **Rollback Strategy**: Revert document edits.

## 4. Database Design Workflow
*   **Objective**: Model data persistence and migration pathways.
*   **Preconditions**: Design requirements showing new entities or fields.
*   **Execution Steps**:
    1.  Draft SQL modifications or SQLAlchemy schemas.
    2.  Verify Normal Form compliance and define indexes.
    3.  Generate Alembic migrations scripts.
*   **Validation**: Execute migration dry-runs on local databases.
*   **Artifacts Produced**: SQLAlchemy code, migration scripts (`backend/database/migrations/`).
*   **Completion Criteria**: Migration run succeeds, tables created safely.
*   **Rollback Strategy**: Run `alembic downgrade -1` or database restore script.

## 5. Backend Development Workflow
*   **Objective**: Implement functional API routes and services.
*   **Preconditions**: Database migration completed, schemas defined.
*   **Execution Steps**:
    1.  Write Pydantic request/response validation schemas.
    2.  Implement business rules and endpoints.
    3.  Inject database sessions and client interfaces.
*   **Validation**: Execute unit test suite, audit logs, run linter tools.
*   **Artifacts Produced**: Endpoint controllers, service helper files.
*   **Completion Criteria**: Tests pass, coverage targets met, API endpoints return mock tests.
*   **Rollback Strategy**: Revert git commits, clean modified routes.

## 6. Frontend Development Workflow
*   **Objective**: Build reactive client dashboard pages.
*   **Preconditions**: Backend endpoint documentation ready.
*   **Execution Steps**:
    1.  Design UI page layout grids.
    2.  Implement styling rules with Tailwind CSS classes.
    3.  Bind data fetching hooks, configure state limits.
*   **Validation**: Audit responsiveness, check Axe accessibility metrics.
*   **Artifacts Produced**: NextJS app routes, React component modules.
*   **Completion Criteria**: Page runs, fetches API values correctly without layout bugs.
*   **Rollback Strategy**: Revert frontend changes.

## 7. AI Pipeline Workflow
*   **Objective**: Orchestrate Vision, OCR, and LLM reasoning.
*   **Preconditions**: Image/text payload structure validated.
*   **Execution Steps**:
    1.  Preprocess image variables.
    2.  Send items requests to Vision AI/OCR models.
    3.  Parse output payload and feed into prompt templates.
    4.  Extract nutritional details or coaching context.
*   **Validation**: Compare accuracy targets with golden test datasets.
*   **Artifacts Produced**: Vision processing code, system prompt parameters.
*   **Completion Criteria**: Parse success rate > 90%, response generated is safe.
*   **Rollback Strategy**: Revert prompts, restore old client libraries.

## 8. Testing Workflow
*   **Objective**: Guarantee quality constraints are satisfied.
*   **Preconditions**: Modified code requiring verification.
*   **Execution Steps**:
    1.  Run Pytest command frameworks.
    2.  Inspect coverage indicators.
    3.  Perform regression checks.
*   **Validation**: Check all tests execute without warnings.
*   **Artifacts Produced**: Coverage reports, test configurations.
*   **Completion Criteria**: Build logs show zero fails, coverage > 85%.
*   **Rollback Strategy**: Debug failures, restore last working revision.

## 9. Bug Fixing Workflow
*   **Objective**: Address defects reported in [KNOWN_ISSUES.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/KNOWN_ISSUES.md).
*   **Preconditions**: Confirmed bug report, test failure.
*   **Execution Steps**:
    1.  Reproduce error behavior locally.
    2.  Write regression unit test.
    3.  Fix code anomaly.
*   **Validation**: Verify regression unit test now succeeds.
*   **Artifacts Produced**: Bugfix branch, updated issue report.
*   **Completion Criteria**: Bug resolved, test verified in CI.
*   **Rollback Strategy**: Revert changes if other tests break.

## 10. Optimization Workflow
*   **Objective**: Improve performance parameters.
*   **Preconditions**: Profiler showing slow queries or latency targets violation.
*   **Execution Steps**:
    1.  Analyze slow spots (e.g. explain queries, track memory logs).
    2.  Implement caching strategies or query optimizations.
*   **Validation**: Re-run load/performance checks.
*   **Artifacts Produced**: Performance log stats, caching updates.
*   **Completion Criteria**: Target latency metrics achieved (e.g. response < 500ms).
*   **Rollback Strategy**: Revert structural code edits if memory leaks or edge anomalies arise.

## 11. Documentation Workflow
*   **Objective**: Prevent knowledge drift in markdown manuals.
*   **Preconditions**: Feature delivery, API update.
*   **Execution Steps**:
    1.  Review code changes.
    2.  Update related API reference parameters or installation details.
*   **Validation**: Check markdown formatting, run lint tests.
*   **Artifacts Produced**: Documentation edits.
*   **Completion Criteria**: Zero broken links, manual matches behavior.
*   **Rollback Strategy**: Restore doc versions via git.

## 12. Deployment Workflow
*   **Objective**: Push software updates to environment servers.
*   **Preconditions**: All branch tests passed.
*   **Execution Steps**:
    1.  Trigger CI build configurations.
    2.  Deploy Docker images.
    3.  Execute DB migrations.
*   **Validation**: Check status metrics of deployed pages.
*   **Artifacts Produced**: System build artifacts, deployment records.
*   **Completion Criteria**: API returned 200 OK, Dashboard renders.
*   **Rollback Strategy**: Roll back server image tag to previous build.

## 13. Release Workflow
*   **Objective**: Merge features into production target branches.
*   **Preconditions**: Production deployment succeeded.
*   **Execution Steps**:
    1.  Create git version tag.
    2.  Compile CHANGELOG entries.
*   **Validation**: Audit changelog records matches tag values.
*   **Artifacts Produced**: Release tags, update [CHANGELOG.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/CHANGELOG.md).
*   **Completion Criteria**: Tag published.
*   **Rollback Strategy**: Delete release tag if blocking issues are found.

## 14. Monitoring Workflow
*   **Objective**: Maintain operational health.
*   **Preconditions**: System active in staging/production.
*   **Execution Steps**:
    1.  Audit logs for error codes.
    2.  Track database and API usage levels.
*   **Validation**: Confirm dashboard uptime is maintained.
*   **Artifacts Produced**: Health status logs.
*   **Completion Criteria**: System running within SLA bounds.
*   **Rollback Strategy**: Restart instances, escalate anomalies to CTO.
