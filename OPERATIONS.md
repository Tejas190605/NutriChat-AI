# Production Operations Manual (OPERATIONS.md)

## Service Architecture
- **Frontend**: Next.js 15+ standalone runner on port 3000
- **Backend**: FastAPI app server on port 8000
- **Database**: PostgreSQL 16 on port 5432
- **Cache**: Redis 7 on port 6379
- **Worker**: Celery background task worker
- **Monitoring**: Prometheus (9090) & Grafana (3001)

## Operational Health Check
- Check backend health: `curl http://localhost:8000/health`
- Check frontend health: `curl http://localhost:3000/`
- View live container logs: `docker compose -f docker-compose.prod.yml logs -f --tail=100`
