# Project Roadmap (ROADMAP.md)

This quarterly roadmap outlines our development and release strategy for NutriChat AI.

---

## Q3 2026: MVP Scaffolding & Core Features (Current)
*   **Goal**: Establish a functional end-to-end WhatsApp intake flow with baseline calorie and macro-nutrient parsing.
*   **Milestones**:
    *   [x] Sprint 1: Workspace setup, governance creation, process bootstrap.
    *   [ ] Sprint 2: Scaffolding API routes, database connections, and migrations.
    *   [ ] Sprint 3: WhatsApp webhook receiver logic, user profile integrations.
    *   [ ] Sprint 4: Vision AI portion calculations, Edamam food search integration.

## Q4 2026: OCR, Memory, & Dashboard Launch
*   **Goal**: Enable pack OCR scans, persistent conversation memory, and open the Admin Dashboard for beta users.
*   **Milestones**:
    *   [ ] Sprint 5: Integrate Vision LLM parsing for packet ingredients and menus.
    *   [ ] Sprint 6: Add dialogue memory caching in Redis so the chatbot remembers user context.
    *   [ ] Sprint 7: Deploy the React/NextJS Admin Dashboard containing statistics charts.
    *   [ ] Sprint 8: Setup Dockerized cloud deployment on AWS.

## Q1 2027: Personal Recommendations & Multimodal Coach
*   **Goal**: Leverage analytics to provide daily macro alternative recommendations and support audio message logging.
*   **Milestones**:
    *   [ ] Sprint 9: Write content-based recommendation logic for dinner ideas.
    *   [ ] Sprint 10: Implement audio voice notes transcription logic for logging meals.
    *   [ ] Sprint 11: Setup periodic health email report digests for users.
    *   [ ] Sprint 12: Perform OWASP security audits and accessibility tuning.
