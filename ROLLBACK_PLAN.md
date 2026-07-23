# Emergency Rollback Plan (ROLLBACK_PLAN.md)

## Rollback Triggers
- Critical system outage (HTTP 5xx rate > 5% for > 5 minutes).
- Database migration corruption or failure.
- Severe security flaw or token leak.

## Instant Mitigation Steps
1. Revert DNS traffic to previous stable IP / backup server.
2. Roll back Docker containers to previous release tag:
   `docker compose -f docker-compose.prod.yml down`
   `git checkout v0.4.0`
   `docker compose -f docker-compose.prod.yml up -d`
3. Restore database snapshot if schema was corrupted:
   `./scripts/restore_db.sh ./backups/<LATEST_STABLE_BACKUP>`
