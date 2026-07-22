# Production Deployment Guide (DEPLOYMENT.md)

This document describes how to deploy the NutriChat AI backend and frontend applications to production environments (Docker + AWS or Render).

---

## 1. System Requirements & Variables

Ensure you have configured the following environment variables in your server configuration:
*   `DATABASE_URL`: Production PostgreSQL URL.
*   `REDIS_URL`: Production Redis cache instance path.
*   `WHATSAPP_TOKEN`: Meta WhatsApp Cloud API credentials.
*   `WHATSAPP_PHONE_NUMBER_ID`: WhatsApp sender ID.
*   `EDAMAM_APP_ID` / `EDAMAM_APP_KEY`: Credentials for nutrition queries.
*   `GEMINI_API_KEY`: API access token.
*   `JWT_SECRET`: High strength signing secret key.

---

## 2. Dockerized Production Deploy

We utilize Docker Compose for orchestrating containers in production environments.

### Step 2.1: Build Production Images
Run the following build command:
```bash
docker-compose -f docker-compose.prod.yml build
```

### Step 2.2: Execute Database Migrations
Initialize database schemas:
```bash
docker-compose -f docker-compose.prod.yml run backend alembic upgrade head
```

### Step 2.3: Start Production Containers
Launch the stack in detached mode:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 3. Deployment on Cloud (AWS/Render)

### Using Render
1.  **PostgreSQL Service**: Provision a production PostgreSQL instance on Render.
2.  **Redis Service**: Provision a production Redis cache instance.
3.  **FastAPI Backend Service**:
    *   Create a Web Service mapping to your repository branch.
    *   Set build command to: `pip install -r backend/requirements.txt`
    *   Set start command to: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 4`
4.  **NextJS Frontend Dashboard**:
    *   Create a static dashboard site or Web Service.
    *   Set build command: `npm run build`
    *   Set start command: `npm run start`

---

## 4. Rollback Strategy
If a deployment fails, run these steps to rollback to the last stable state:
1.  Revert the main container tag locally.
2.  Push tag configurations to deployment runners.
3.  If schema changes need rollback, execute database migration downgrades:
    ```bash
    alembic downgrade -1
    ```
4.  Verify system uptime via checking the `/health` endpoint.
5.  Log any rollback events inside [CHANGELOG.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/CHANGELOG.md).
