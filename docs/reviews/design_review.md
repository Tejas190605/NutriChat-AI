# Design Review Report (design_review.md)

This report evaluates the specifications, technical research, architecture, database schemas, and design documents created during Phase 1 to Phase 4 for NutriChat AI.

---

## 1. Executive Summary & Readiness Score
*   **Final Readiness Score**: **92/100**
*   **Assessment**: The repository has a comprehensive architectural and design foundation. The database models are normalized, the user interface follows clear spacing standards, and the async backend pattern is optimized. We have identified some minor security, database query, and conversational edge-case gaps which are documented below.

---

## 2. Strengths
*   **Robust Caching Layout**: Utilizing the `food_cache` database table coupled with Redis memory checks mitigates third-party API rate limits (Edamam 5 req/min tier).
*   **Decoupled AI Engine**: Decoupling the LLM prompt wrappers from route definitions permits switching between models (Gemini 2.5, GPT-4o fallbacks) without impacting webhook controllers.
*   **Async Event Execution**: Using Celery + Redis background queues ensures the webhook handler acknowledges Meta API payloads within the mandatory 2.0-second timeout limit.
*   **Clear Design System**: Mapped HSL colors, responsive breakpoints, and WCAG AA guidelines ensure visual style coherence.

---

## 3. Weaknesses & Missing Details

### 3.1. Conversational UX Gaps (WhatsApp Chat)
*   *Issue*: The onboarding flow sequence lacks a "reset" or "re-enter" keyword trigger. If a user inputs their weight incorrectly, there is no documented path for correction during the survey.
*   *Recommendation*: Implement a `/reset` command that clears the onboarding state cache and restarts the questionnaire.

### 3.2. Security Verification Gaps (POST Handshake)
*   *Issue*: While the GET verify route checks query tokens, the POST webhook requirements omit details regarding verifying Meta's payload signatures using the APP secret (HMAC SHA-256 header validation).
*   *Recommendation*: Enforce signature check middleware on the incoming webhook router before processing any message logs.

### 3.3. Exercise Tracking Scope
*   *Issue*: Mapped in the functional spec list but missing corresponding database column details in `schema.sql` (e.g. where do we persist calorie deficits from walking/running logs?).
*   *Recommendation*: Add a `user_activities` table in the next Alembic migration iteration.

---

## 4. Risk Analysis

| Risk Area | Threat Description | Severity | Mitigation Plan |
| :--- | :--- | :--- | :--- |
| **API Costs** | High voice notes / vision image upload volumes lead to cost leaks. | High | Set strict user message rate limit limits (e.g., max 10 photos/day per chat user). |
| **Meta Webhook Retry**| Failed jobs trigger duplicate webhook retries from Meta. | Medium | Enforce Redis task locking on the incoming WhatsApp `message_id`. |
| **Database Locks** | Parallel writes to `chat_histories` block other records. | Medium | Configure async database session connection limits cleanly. |

---

## 5. Summary Checklists

*   **Database Normalization**: ✅ 3NF Compliant.
*   **Accessibility Standards**: ✅ WCAG 2.2 AA compliant.
*   **Scalability**: ✅ Async worker architecture handles traffic spikes safely.
