# Incident Response Runbook (RUNBOOK.md)

## Emergency Procedures

### 1. High API Error Rate (> 1%)
1. Inspect backend error trace logs:
   `docker logs nutrichat-prod-backend --tail 200`
2. Check database connection pool status.
3. Restart backend service if deadlocked:
   `docker compose -f docker-compose.prod.yml restart backend`

### 2. Redis Cache & Queue Disconnection
1. Verify Redis process health:
   `docker exec nutrichat-prod-redis redis-cli ping`
2. Restart Redis container:
   `docker compose -f docker-compose.prod.yml restart redis`
