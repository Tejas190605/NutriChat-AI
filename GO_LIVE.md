# Go-Live Execution Plan (GO_LIVE.md)

## T-Minus 60 Minutes: Pre-Flight Audit
1. Verify database snapshot backup is completed:
   `./scripts/backup_db.sh`
2. Check CI/CD GitHub Actions pipeline status (All green).

## T-Minus 30 Minutes: Infrastructure Provisioning
1. Spin up production containers:
   `docker compose -f docker-compose.prod.yml up -d --build`
2. Run database migration check:
   `docker exec nutrichat-prod-backend poetry run alembic upgrade head`

## T-Minus 10 Minutes: Smoke Tests
1. Test GET `/api/v1/health` endpoint -> 200 OK.
2. Test WhatsApp Webhook GET challenge verification -> 200 OK.
3. Test Next.js user portal login & meal logging flows.

## T-Minus 0 Minutes: Go-Live
1. Update DNS routing to point live traffic to NGINX / Cloud IP.
2. Enable WhatsApp production Meta Cloud Webhook.
