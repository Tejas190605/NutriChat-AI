# Security Policy & Hardening (SECURITY.md)

## Security Controls
- **JWT Authentication**: Short-lived bearer tokens (24h) with Argon2 credential hashing.
- **HTTP Security Headers**: Strict Transport Security (HSTS), X-Frame-Options (DENY), Content-Security-Policy (CSP), X-Content-Type-Options (nosniff).
- **Container Privileges**: All Docker runtime containers execute as non-root users (`appuser` / `nextjs`).
- **Webhook Integrity**: Meta WhatsApp Cloud API webhooks verify `X-Hub-Signature-256` HMAC signatures before processing.
