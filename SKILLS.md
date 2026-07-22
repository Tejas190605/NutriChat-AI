# Reusable AI Engineering Skills (SKILLS.md)

This catalog defines the standard operational skills utilized by the autonomous AI organization to build and maintain the NutriChat AI project.

---

## 1. System Design
*   **Purpose**: Design system component boundaries and interaction models.
*   **When to use**: Before creating new major modules or features.
*   **Inputs**: Feature specification, architectural patterns.
*   **Outputs**: Topology map, design specifications.
*   **Quality Checklist**:
    *   [ ] Checked component boundary isolation.
    *   [ ] Ensured single points of failure are mitigated.
*   **Best Practices**: Use loose coupling, define clean API contracts, prioritize simplicity.

## 2. Architecture Review
*   **Purpose**: Assess implementation plans against established patterns.
*   **When to use**: During architecture design phases.
*   **Inputs**: Design document, current system state.
*   **Outputs**: Review feedback report.
*   **Quality Checklist**:
    *   [ ] Checked DRY compliance.
    *   [ ] Verified alignment with [RULES.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/RULES.md).
*   **Best Practices**: Audit dependencies closely, prevent scope leak.

## 3. Backend Development
*   **Purpose**: Write core backend server logic.
*   **When to use**: When implementing backend endpoints, business logic, or services.
*   **Inputs**: Requirements, database models, Pydantic schemas.
*   **Outputs**: Checked, type-safe Python code.
*   **Quality Checklist**:
    *   [ ] Handled exceptions properly.
    *   [ ] Added type hints.
*   **Best Practices**: Write clean docstrings, use python standard practices.

## 4. Frontend Development
*   **Purpose**: Write client interface components.
*   **When to use**: When implementing dashboard UI.
*   **Inputs**: UX wireframe diagrams, styles, APIs.
*   **Outputs**: Reusable React/Next.js files.
*   **Quality Checklist**:
    *   [ ] Checked responsive scaling on mobile.
    *   [ ] Validated layout variables.
*   **Best Practices**: Keep components small, use functional rendering hooks.

## 5. FastAPI
*   **Purpose**: Implement asynchronous APIs.
*   **When to use**: Creating routers, middleware, and schemas.
*   **Inputs**: Route requirements, body schemas.
*   **Outputs**: FastAPI endpoint logic.
*   **Quality Checklist**:
    *   [ ] Declared Pydantic validation checks.
    *   [ ] Verified async operation loop safety.
*   **Best Practices**: Leverage dependencies for shared logic (auth, database).

## 6. React
*   **Purpose**: Build interactive dashboard elements.
*   **When to use**: Designing client layouts.
*   **Inputs**: Next layouts, state parameters.
*   **Outputs**: Interactive UI components.
*   **Quality Checklist**:
    *   [ ] Optimized rendering paths.
    *   [ ] Handled component state isolation.
*   **Best Practices**: Avoid mutating state directly, use memoization (useMemo, useCallback) when appropriate.

## 7. NextJS
*   **Purpose**: Implement server-side rendering and routing.
*   **When to use**: Building dashboard pages.
*   **Inputs**: Routing structure, API data.
*   **Outputs**: SSR and static dashboard views.
*   **Quality Checklist**:
    *   [ ] Used Image component for optimizations.
    *   [ ] Verified routing configuration files.
*   **Best Practices**: Use Server Components by default; opt-in to Client Components only when interactive.

## 8. Tailwind CSS
*   **Purpose**: Style dashboard components fluidly.
*   **When to use**: Building pages and styling elements.
*   **Inputs**: Style guide tokens, UI mockups.
*   **Outputs**: Tailwind style definitions.
*   **Quality Checklist**:
    *   [ ] Checked theme variables alignment.
    *   [ ] Verified dark/light mode switches.
*   **Best Practices**: Define custom colors in config, use responsive breakpoints.

## 9. Docker
*   **Purpose**: Package system modules into virtualized containers.
*   **When to use**: Creating build profiles or compose environments.
*   **Inputs**: Source code paths, lockfiles, runtime configs.
*   **Outputs**: Dockerfiles, Docker Compose scripts.
*   **Quality Checklist**:
    *   [ ] Used multi-stage builds.
    *   [ ] Kept base image sizes minimized.
*   **Best Practices**: Do not run as root inside containers, leverage image layer caching.

## 10. PostgreSQL
*   **Purpose**: Implement data modeling and queries.
*   **When to use**: Modifying schema, writing complex SQL.
*   **Inputs**: ERD specification, performance constraints.
*   **Outputs**: SQL files, migrations.
*   **Quality Checklist**:
    *   [ ] Checked database indexing.
    *   [ ] Verified transaction safety.
*   **Best Practices**: Use parameter binding, avoid complex loops in database functions.

## 11. Redis
*   **Purpose**: Setup caching, session memory, and rate limits.
*   **When to use**: High traffic webhook storage, session data caching.
*   **Inputs**: Dynamic data structures, TTL specifications.
*   **Outputs**: Redis client queries, cache config files.
*   **Quality Checklist**:
    *   [ ] Configured proper TTL parameters.
    *   [ ] Handled connection failures gracefully.
*   **Best Practices**: Keep key naming structure simple and descriptive.

## 12. Git
*   **Purpose**: Track and version codebase history.
*   **When to use**: Tracking feature changes, committing code.
*   **Inputs**: File updates, change lists.
*   **Outputs**: Git commits, clean branch histories.
*   **Quality Checklist**:
    *   [ ] Avoided staging secret configurations.
    *   [ ] Handled conflicts carefully.
*   **Best Practices**: Write conventional commit messages, squash local commits before push.

## 13. GitHub
*   **Purpose**: Coordinate repository pull requests and pipelines.
*   **When to use**: Creating branches, requesting code reviews.
*   **Inputs**: Branch updates, PR specs.
*   **Outputs**: Dynamic code reviews, merge records.
*   **Quality Checklist**:
    *   [ ] Checked branch protection status.
    *   [ ] Confirmed action runners are active.
*   **Best Practices**: Write clean pull request descriptions, tag reviews clearly.

## 14. CI/CD
*   **Purpose**: Automate pipelines for build, test, and release tasks.
*   **When to use**: Standardizing validation actions.
*   **Inputs**: YAML workflows, runner triggers.
*   **Outputs**: Pipeline build status.
*   **Quality Checklist**:
    *   [ ] Setup parallel testing execution.
    *   [ ] Handled secret masks.
*   **Best Practices**: Fail fast, cache dependencies, run security scans automatically.

## 15. Testing
*   **Purpose**: Validate code behavior against specifications.
*   **When to use**: Writing tests for endpoints, modules, and components.
*   **Inputs**: Specs, source files.
*   **Outputs**: Pytest scripts, test reports.
*   **Quality Checklist**:
    *   [ ] Target coverage of > 85% achieved.
    *   [ ] Checked boundary cases.
*   **Best Practices**: Write independent tests, isolate external APIs with mock clients.

## 16. Debugging
*   **Purpose**: Identify and resolve software bugs.
*   **When to use**: Fixing issues listed in [KNOWN_ISSUES.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/KNOWN_ISSUES.md).
*   **Inputs**: Log files, error stacktraces.
*   **Outputs**: Resolved bugs report, bugfix patches.
*   **Quality Checklist**:
    *   [ ] Added test validating the fix.
    *   [ ] Checked for regressions.
*   **Best Practices**: Use binary search debugging, trace state variables, review error logs first.

## 17. Refactoring
*   **Purpose**: Restructure codebase layout without changing core outputs.
*   **When to use**: Resolving style issues, improving performance.
*   **Inputs**: Existing files, target patterns.
*   **Outputs**: Optimized cleaner source files.
*   **Quality Checklist**:
    *   [ ] Checked regression tests status.
    *   [ ] Verified code style constraints.
*   **Best Practices**: Perform small, incremental commits; verify at each step.

## 18. Security Audit
*   **Purpose**: Scan database, routes, and packages for safety loopholes.
*   **When to use**: Before major production releases.
*   **Inputs**: Dependency lists, router endpoints.
*   **Outputs**: Security reports, sanitization suggestions.
*   **Quality Checklist**:
    *   [ ] Checked for SQL injection vulnerability.
    *   [ ] Verified API key encryption rules.
*   **Best Practices**: Follow OWASP checklist, run security checks during build pipelines.

## 19. Performance Optimization
*   **Purpose**: Reduce memory usage and execution latency.
*   **When to use**: Bottlenecks in API endpoints, slow queries.
*   **Inputs**: Performance profiles, metrics.
*   **Outputs**: Optimized code files, cache configs.
*   **Quality Checklist**:
    *   [ ] Tested throughput under heavy loads.
    *   [ ] Verified page sizes are minimal.
*   **Best Practices**: Profile code before optimizing, select index patterns based on queries.

## 20. Prompt Engineering
*   **Purpose**: Draft system instructions to shape model behaviors.
*   **When to use**: Modifying chatbot responses, structuring outputs.
*   **Inputs**: User input logs, task specs.
*   **Outputs**: Clean, optimized prompt scripts.
*   **Quality Checklist**:
    *   [ ] Tested prompt against injection variants.
    *   [ ] Handled edge inputs context.
*   **Best Practices**: Give clear instructions, include few-shot examples, separate instructions from variables.

## 21. LLM Integration
*   **Purpose**: Interface with generative APIs (Gemini/GPT).
*   **When to use**: Calling AI clients for reasoning, extraction.
*   **Inputs**: Prompt templates, API parameters.
*   **Outputs**: Parsed model responses.
*   **Quality Checklist**:
    *   [ ] Handled API rate limit exceptions.
    *   [ ] Set appropriate fallback models.
*   **Best Practices**: Monitor API latency, validate schemas of returned outputs.

## 22. OCR
*   **Purpose**: Extract textual details from food packet labels.
*   **When to use**: Processing nutrition labels.
*   **Inputs**: Clean ingredient/label photos.
*   **Outputs**: Structured JSON mappings.
*   **Quality Checklist**:
    *   [ ] Preprocessed images for optimal contrast.
    *   [ ] Checked format validation on outputs.
*   **Best Practices**: Match text output structure with a predefined schema.

## 23. Computer Vision
*   **Purpose**: Identify food shapes and estimate volumes.
*   **When to use**: Meal logging via image webhooks.
*   **Inputs**: Meal photo streams.
*   **Outputs**: Food items classifications, portion sizes.
*   **Quality Checklist**:
    *   [ ] Normalized images before inference.
    *   [ ] Validated confidence score thresholds.
*   **Best Practices**: Handle multiple dishes in single plates gracefully.

## 24. REST API Design
*   **Purpose**: Construct developer-friendly API schemas.
*   **When to use**: Creating route endpoints.
*   **Inputs**: Data payloads, access requirements.
*   **Outputs**: OpenAPI definitions, route files.
*   **Quality Checklist**:
    *   [ ] Used standard HTTP status codes.
    *   [ ] Kept naming conventions consistent.
*   **Best Practices**: Version API routes, use standard error formats.

## 25. Documentation
*   **Purpose**: Keep technical manuals up-to-date.
*   **When to use**: Updates in codebase, workflows, or setup steps.
*   **Inputs**: Feature code updates.
*   **Outputs**: Clear, updated markdown files.
*   **Quality Checklist**:
    *   [ ] Verified file links and cross-references.
    *   [ ] Cleaned old deprecated commands.
*   **Best Practices**: Keep manuals descriptive but concise, keep code blocks updated.

## 26. Deployment
*   **Purpose**: Deploy changes to staging/production servers.
*   **When to use**: Release execution steps.
*   **Inputs**: Build containers, environment configuration.
*   **Outputs**: Active production URLs.
*   **Quality Checklist**:
    *   [ ] Verified status endpoints response.
    *   [ ] Confirmed logs pipeline works.
*   **Best Practices**: Use zero-downtime rolling updates, backup databases before changes.
