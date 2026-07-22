# Security Policy (SECURITY.md)

This document outlines the security policies, secrets management directives, authentication designs, and audit standards for NutriChat AI.

---

## 1. Security Policy & Disclosures
We take security issues seriously. If you find a security vulnerability, please do not file a public issue. Instead, report it privately to: `security@nutrichat.ai`.

---

## 2. Secrets Management
*   **Zero Exposed Secrets Policy**: Never commit credentials, client tokens, private keys, database connection strings, or password hashes to version control.
*   **Configuration Isolation**: Load all variables through environment containers (`.env` files) loaded locally and managed inside host runners (Docker/AWS).
*   **Variable Validation**: Run validation schemas on server startup using Pydantic Settings modules to confirm all variables are set and meet length/format standards.

---

## 3. Authentication Design
*   **WhatsApp Webhook Validation**: Authenticate WhatsApp hook interactions using custom webhook tokens supplied during integration registration.
*   **Dashboard Authentication**: Access to the Admin Dashboard requires standard JWT (JSON Web Token) authentication:
    *   *Password Cryptography*: Hashed using high-strength bcrypt schemes.
    *   *Tokens expiration*: Tokens are signed with HS256 algorithms and expire in 2 hours.
    *   *Transmission security*: Transport tokens exclusively inside HTTPS secure, HttpOnly, SameSite cookies.

---

## 4. OWASP Checklist for NutriChat AI
All backend endpoints and database scripts must conform to this quality check list:
*   [ ] **SQL Injection Prevention**: Utilize SQLAlchemy parameters binding exclusively. No raw string manipulation in queries.
*   [ ] **Cross-Site Scripting (XSS)**: Sanitize string parameters prior to frontend rendering or storage database insertion.
*   [ ] **Broken Object Level Authorization (BOLA)**: Always verify that the authenticated userID matches the requested mealLog ID parameter.
*   [ ] **Rate Limiting**: Rate limit public API endpoints using Redis token bucket middleware filters (e.g. limit WhatsApp webhooks to 5 requests/sec per user).
*   [ ] **Data Transit Encryption**: Force all external web interactions through HTTPS SSL rules.
*   [ ] **Sensitive Data at Rest**: Encrypt personal health information configurations in database storage fields when requested.
