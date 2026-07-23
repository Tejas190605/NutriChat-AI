# Production Deployment Guide (DEPLOYMENT.md)

## Overview
This guide documents deploying NutriChat AI using Docker Compose in production environments.

## Prerequisites
- Linux Server (Ubuntu 22.04 LTS recommended)
- Docker 24.0+ & Docker Compose v2.20+
- Domain with SSL certificate (Let's Encrypt / NGINX reverse proxy)

## Deployment Steps
1. Clone repository:
   ```bash
   git clone https://github.com/nutrichat/NutriChat-AI.git
   cd NutriChat-AI
   ```

2. Configure production environment variables:
   ```bash
   cp .env.production.example .env
   nano .env
   ```

3. Launch Docker Compose Production cluster:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```

4. Verify service health:
   ```bash
   docker compose -f docker-compose.prod.yml ps
   ```
