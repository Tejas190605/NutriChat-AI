# Backup & Disaster Recovery Guide (BACKUP.md)

## Automated Backups
- **Database Backup**: Daily `pg_dump` compressed with `gzip`.
- **Redis Snapshot**: Daily RDB persistence snapshot.

## Trigger Backup Manually
```bash
./scripts/backup_db.sh
```

## Disaster Recovery Restore
```bash
./scripts/restore_db.sh ./backups/20260723_120000
```
