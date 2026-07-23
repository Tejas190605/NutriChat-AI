# Release Blockers & External Infrastructure Audit (RELEASE_BLOCKERS.md)

## Summary Statement
> **"The repository is feature complete. Remaining work requires deployment credentials and production infrastructure rather than additional software development."**

---

## Task 1 & 2 — External Infrastructure Requirements

| Requirement | Current Status | Why It Is Needed | Where It Is Configured | Action Required |
| :--- | :--- | :--- | :--- | :--- |
| **Google Gemini API Key** | Placeholder (`dev_gemini_key`) | Conversational AI health coach brain, vision meal detection, and nutrition reasoning. | `.env` / `GEMINI_API_KEY` | Create GCP project, enable Gemini API, populate production key. |
| **Meta WhatsApp Cloud API** | Placeholder (`dev_facebook_app_secret`) | Primary messaging user interface for WhatsApp meal logging and notification delivery. | `.env` / `FACEBOOK_APP_SECRET` | Create Meta Business App, register phone number, set webhook URL. |
| **Cloudinary Media Storage** | Placeholder (`dev_cloud`) | Persistent storage and CDN image optimization for meal photos and OCR scans. | `.env` / `CLOUDINARY_URL` | Register Cloudinary account, copy API key and secret credentials. |
| **Managed PostgreSQL Database** | Local Host (`localhost:5432`) | Normalized relational database storing users, profiles, meals, summaries, and chat history. | `.env` / `DATABASE_URL` | Provision Render/AWS PostgreSQL database, run Alembic migrations. |
| **Managed Redis Instance** | Local Host (`localhost:6379`) | Session caching, rate limiting, and Celery background task broker. | `.env` / `REDIS_URL` | Provision managed Redis cluster with password authentication. |
| **Domain Names (DNS)** | Not Pointed | Production entry points (`app.nutrichat.ai` and `api.nutrichat.ai`). | DNS Registrar / NGINX | Add A/CNAME DNS records pointing to load balancer IP address. |
| **SSL / TLS Certificates** | Not Issued | Enforce HTTPS encryption for API security and Web Push Service Workers. | `deploy/nginx.conf` | Issue Let's Encrypt SSL certificates via Certbot. |
| **Cloud Hosting Accounts** | Local Environment | Host FastAPI backend, Next.js frontend, Celery workers, and NGINX proxy. | `render.yaml` / `fly.toml` | Create Render or AWS account and trigger production deployment. |

---

## Task 3 — Remaining Manual Setup Tasks Before Launch

1. **Configure Production Environment Variables**: Populate `.env.production` with live secrets and credentials.
2. **Point DNS Records**: Configure A and CNAME records for `app.nutrichat.ai` and `api.nutrichat.ai`.
3. **Verify Meta WhatsApp Webhook**: Register webhook URL and test `X-Hub-Signature-256` HMAC validation token.
4. **Configure Cloudinary CDN**: Set up production image transformation buckets.
5. **Configure Gemini Billing & Quotas**: Set up spending alerts in Google Cloud Console.
6. **Schedule Database Backups**: Enable cron task executing `scripts/backup_db.sh`.
7. **Configure Telemetry Alerts**: Import `monitoring/grafana/dashboards.json` into Grafana and set error rate alerts.

---

## Task 5 — Release Blockers List

### 1. Missing Production Secret Keys
- **Severity**: Critical (P1)
- **Description**: Environment variables for JWT secret, database passphrases, and Redis passwords are set to development defaults.
- **Owner**: DevOps Lead
- **Estimated Effort**: 30 minutes
- **Required Credentials**: Production secret generator output.

### 2. Unregistered WhatsApp Business Phone Number
- **Severity**: Critical (P1)
- **Description**: WhatsApp webhook receiver requires a verified Meta Business Account phone number.
- **Owner**: Product Owner / Business Analyst
- **Estimated Effort**: 2 hours
- **Required Credentials**: Meta Developer Portal App ID, App Secret, and Verify Token.

### 3. Missing Managed Database & Cache Services
- **Severity**: Critical (P1)
- **Description**: Cloud hosting requires live managed PostgreSQL 16 and Redis 7 connection URLs.
- **Owner**: Infrastructure Architect
- **Estimated Effort**: 1 hour
- **Required Credentials**: Cloud provider database connection strings.
