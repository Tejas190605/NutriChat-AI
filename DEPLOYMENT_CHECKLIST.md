# Production Deployment Checklist (DEPLOYMENT_CHECKLIST.md)

This checklist tracks every manual setup and verification step required prior to cutting over to live production traffic.

---

## Pre-Launch Verification Matrix

### Infrastructure & Cloud Host
- [ ] Provision production cloud account (Render / AWS / Fly.io).
- [ ] Deploy Docker containers using `docker-compose.prod.yml` or `render.yaml`.
- [ ] Verify health check endpoints (`/health` and `/`).

### Secrets & Environment Security
- [ ] Populate `.env.production` with a minimum 64-character `JWT_SECRET`.
- [ ] Configure `REDIS_PASSWORD` and database passphrases.
- [ ] Remove all default development environment variables.

### Managed Database (PostgreSQL)
- [ ] Provision managed PostgreSQL 16 database instance.
- [ ] Run Alembic migrations (`poetry run alembic upgrade head`).
- [ ] Verify foreign key constraints and index performance on `users`, `meals`, `chat_messages`.

### Managed Cache & Broker (Redis)
- [ ] Provision managed Redis 7 instance with AOF persistence enabled.
- [ ] Verify Celery worker queue connection to Redis broker.

### AI Engine APIs (Google Gemini)
- [ ] Enable billing on Google Cloud Platform for Gemini 1.5/2.0 API.
- [ ] Configure `GEMINI_API_KEY` in environment secrets.
- [ ] Set up quota alert thresholds in Google Cloud Console.

### WhatsApp Cloud API (Meta Developer Platform)
- [ ] Register production WhatsApp Business Phone Number in Meta Developer Portal.
- [ ] Configure Webhook URL (`https://api.nutrichat.ai/api/v1/webhook`).
- [ ] Verify `X-Hub-Signature-256` HMAC SHA-256 signature verification token.

### Vision & OCR Media Pipeline (Cloudinary)
- [ ] Register Cloudinary production storage account.
- [ ] Configure `CLOUDINARY_URL` / `CLOUDINARY_API_KEY` / `CLOUDINARY_API_SECRET`.
- [ ] Test image upload and resizing transformations.

### Monitoring & Telemetry
- [ ] Verify Prometheus scraper scraping `/metrics` on backend port 8000.
- [ ] Import `monitoring/grafana/dashboards.json` into Grafana instance.
- [ ] Configure alert notifications for high latency (> 500ms) or 5xx error spikes.

### Disaster Recovery & Backups
- [ ] Verify `scripts/backup_db.sh` daily cron execution.
- [ ] Test database restoration script (`scripts/restore_db.sh`) in staging environment.

### Domain & SSL Certificates
- [ ] Configure DNS A and CNAME records pointing to NGINX load balancer IP.
- [ ] Issue Let's Encrypt SSL/TLS certificates for `app.nutrichat.ai` and `api.nutrichat.ai`.
- [ ] Verify HTTPS redirection and security headers (`HSTS`, `CSP`, `X-Frame-Options`).

### Pre-Launch Smoke Tests & Rollback
- [ ] Execute user registration, login, meal logging, and AI coach chat smoke tests.
- [ ] Test rollback execution script in case of emergency migration failure.
