#!/bin/bash
# NutriChat AI Production Database Restoration Script

set -e

if [ -z "$1" ]; then
  echo "Usage: ./scripts/restore_db.sh <path_to_backup_dir>"
  exit 1
fi

BACKUP_DIR="$1"

echo "Restoring PostgreSQL database from $BACKUP_DIR/db_dump.sql.gz..."
gunzip -c "$BACKUP_DIR/db_dump.sql.gz" | docker exec -i nutrichat-prod-db psql -U ${POSTGRES_USER:-postgres} ${POSTGRES_DB:-nutrichat}

echo "PostgreSQL restoration complete!"
