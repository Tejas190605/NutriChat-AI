# Project Risk Register (RISK_REGISTER.md)

This log details the identified technical, business, and security risks for NutriChat AI, along with their mitigation plans.

---

## 1. Technical Risks

### Risk T-01: Inaccurate food volume or calorie estimation by Vision AI
*   **Likelihood**: High | **Impact**: High
*   **Description**: The Vision model might estimate portion sizes incorrectly (e.g. interpreting a deep dish pizza slice as standard or estimating weight margins with > 30% error).
*   **Mitigation Strategy**: Implement interactive confirmation steps over WhatsApp. Instead of locking the estimated macros immediately, send a prompt back to the user: *"I calculated 2 slices of cheese pizza (~240g, 580 kcal). Does that look correct?"*, allowing them to refine the weight or count manually.

### Risk T-02: Third-party API rate limitations and timeouts
*   **Likelihood**: Medium | **Impact**: High
*   **Description**: Edamam or WhatsApp Cloud API rate limits are hit during peak usage, dropping webhook events.
*   **Mitigation Strategy**: Incorporate Redis caching. Cache queries for common food items. Build a message retry queue with exponential backoff inside the FastAPI backend.

---

## 2. Business Risks

### Risk B-01: High usage costs for Vision LLMs (GPT-4V / Gemini)
*   **Likelihood**: Medium | **Impact**: High
*   **Description**: Processing thousands of images per day leads to high token costs.
*   **Mitigation Strategy**: Cache food classification matches. Before calling the heavy vision LLM, compute an image hash check to see if an identical photo has been parsed recently. Set daily user limits on image analysis messages (e.g. max 10 photos/day per user on standard tiers).

---

## 3. Security Risks

### Risk S-01: Leak of user health profiles or meal logs data
*   **Likelihood**: Low | **Impact**: High
*   **Description**: Unauthorized actors bypass auth to access private user health logs database.
*   **Mitigation Strategy**: Enforce strict BOLA authorization checks on all query parameters. Isolate database instances in private cloud VPC subnets with no public IP routes. Implement AES-256 field encryption for columns storing high-sensitivity user health profiles.
