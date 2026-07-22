# Changelog (CHANGELOG.md)

All notable changes to the NutriChat AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

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
