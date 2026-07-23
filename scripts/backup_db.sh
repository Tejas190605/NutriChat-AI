#!/bin/bash
# NutriChat AI Production Database & Redis Backup Script

set -e

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "Starting PostgreSQL backup..."
docker exec nutrichat-prod-db pg_dump -U ${POSTGRES_USER:-postgres} ${POSTGRES_DB:-nutrichat} | gzip > "$BACKUP_DIR/db_dump.sql.gz"

echo "Starting Redis dump..."
docker exec nutrichat-prod-redis redis-cli save
docker cp nutrichat-prod-redis:/data/dump.rdb "$BACKUP_DIR/redis_dump.rdb"

echo "Backup complete! Saved artifacts to $BACKUP_DIR"
