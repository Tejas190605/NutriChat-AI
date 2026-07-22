# Non-Functional Requirements Specification (non_functional_requirements.md)

This specification defines the quality attributes, security boundaries, performance parameters, and compliance guidelines for NutriChat AI.

---

## 1. Uptime, Reliability, & Availability

*   **Availability SLA**: Target **99.9%** uptime for API routers and the NextJS web dashboard.
*   **Database Backup Policy**: Automated daily snapshot backups of the PostgreSQL instance stored securely in isolated AWS S3 buckets, retained for 30 days.
*   **API Outage Resilience**: If third-party APIs (Edamam, Open Food Facts) are unreachable, the system must degrade gracefully:
    *   Inform the user via WhatsApp: *"I'm currently unable to retrieve nutritional metrics, but I have logged your meal name. I will update you as soon as the service recovers."*
    *   Retry scheduled calls in background queues using Celery backoff.

---

## 2. Performance & Scalability

*   **Webhook Response Latency**: The webhook server must acknowledge incoming Meta payloads within **2.0 seconds** (returning HTTP 200 OK) to prevent Meta from retrying webhook delivery.
*   **Signature Verification Overhead**: Webhook signature verification using HMAC-SHA256 must execute in under **5ms** so as not to bottleneck the 2s webhook ACK SLA bounds.
*   **Message Processing Latency**: The complete end-to-end processing (fetching image, Vision AI classification, Edamam lookup, database logging, generating response text) must complete within **8.0 seconds** for 95% of requests.
*   **Concurrent Users**: Support up to **100 concurrent webhook events** without thread starvation. Set FastAPI workers to `cpu_cores * 2 + 1`.

---

## 3. Security & Compliance

*   **Webhook Payload Security**: Mandatory validation of `X-Hub-Signature-256` header on all inbound webhook messages. Payloads missing signatures or with mismatched hashes must be dropped immediately with a 401 Unauthorized response code.
*   **Credential Protection**: The Facebook App Secret must be stored in production vault managers and loaded dynamically as a masked environment variable (`FACEBOOK_APP_SECRET`).
*   **Transport Layer Security**: Force HTTPS on all incoming and outgoing connections using TLS 1.3 protocol standards.
*   **Data Encryption**:
    *   *At rest*: Encrypt columns containing personal user parameters (weight, height, activity level, health goals) inside PostgreSQL using AES-256 standard encryption keys.
    *   *In transit*: API tokens, database connection logs, and third-party keys must travel encrypted.
*   **Rate Limits**:
    *   Limit public webhook endpoints to **5 requests per second** per phone number ID using Redis token buckets.
    *   Dashboard logins limited to **5 attempts per minute** before temporary IP lockouts.

---

## 4. Maintainability & Code Quality

*   **Code Coverage**: Automated unit test suites must cover at least **85%** of lines.
*   **Static Checks**: Zero MyPy typing compilation warnings, zero Flake8/Ruff style errors.
*   **Audit Logging**: Every access to user health tables, system logins, configuration changes, or webhook exceptions must write to structural system logs.
