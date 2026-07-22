# Software Architecture (ARCHITECTURE.md)

This document describes the high-level system architecture, component integrations, data flows, and AI pipeline topology for NutriChat AI.

---

## 1. System Components Overview

The system consists of three main segments:
1.  **Client Channel**: User communicates exclusively through WhatsApp using text, images, or voice inputs.
2.  **API Backend Server**: FastAPI asynchronous server managing webhooks, database persistence, caching, and AI logic coordination.
3.  **Admin Dashboard**: NextJS dashboard reporting analytics, system logs, database stats, and active sessions.

```mermaid
graph TD
    User([User WhatsApp Client]) -->|Send Text/Voice/Image| MetaWhatsAppAPI[Meta WhatsApp Cloud API]
    MetaWhatsAppAPI -->|JSON webhook payload| FastAPI[FastAPI Backend]
    
    subgraph FastAPI Backend App
        API_Route[Webhook Endpoint] --> Auth[Auth check & Request Sanitizer]
        Auth --> Caching{Redis Deduplication}
        Caching -->|New Request| AIPipeline[AI Pipeline Coordinator]
        Caching -->|Duplicate| Ignore[Ignore Payload]
        
        AIPipeline --> VisionEngine[Vision & OCR Client]
        AIPipeline --> LLMEngine[LLM Coach Brain]
        AIPipeline --> RecommendationEngine[Meal & Alternatives Router]
        
        FastAPI --> SQLAlchemy[SQLAlchemy ORM]
    end

    SQLAlchemy -->|Read/Write| PostgreSQL[(PostgreSQL Database)]
    VisionEngine -->|Fetch External Macros| Edamam[Edamam & Open Food API]
    NextJS[NextJS Admin Dashboard] -->|API Requests| FastAPI
```

---

## 2. Webhook & Message Sequence Flow

Below is the workflow sequence when a food photo is sent by a user:

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Meta as Meta Cloud API
    participant Webhook as FastAPI Webhook
    participant DB as PostgreSQL
    participant AI as Vision/LLM Engine
    participant Nutrition as Edamam API

    User->>Meta: Sends Food Photo (Pizza)
    Meta->>Webhook: Webhook Payload (HTTP POST)
    Webhook-->>Meta: 200 OK (Acknowledge)
    Webhook->>DB: Fetch User Profile (Height, Target Cal)
    DB-->>Webhook: Return Profile (Target: 2000 kcal)
    Webhook->>AI: Send Image to Vision AI
    AI->>AI: Extract food name ("Pizza") & Portion ("2 slices")
    Webhook->>Nutrition: Request Macros for "2 slices pizza"
    Nutrition-->>Webhook: Return Calories (580 kcal), Protein (24g)
    Webhook->>DB: Log Meal entry
    Webhook->>AI: Generate coach reply (incorporate targets deficit)
    AI-->>Webhook: Return conversational text response
    Webhook->>Meta: Send message template
    Meta->>User: Renders coach WhatsApp message text
```

---

## 3. Database ERD (Entity Relationship Diagram)

```mermaid
erDiagram
    USERS ||--o{ MEALS : "logs"
    USERS ||--o{ CHAT_HISTORIES : "stores"
    USERS ||--o{ NOTIFICATIONS : "manages"

    USERS {
        UUID id PK
        VARCHAR name
        DECIMAL height
        DECIMAL weight
        VARCHAR goal
        VARCHAR activity_level
        TIMESTAMP created_at
    }

    MEALS {
        UUID id PK
        UUID user_id FK
        VARCHAR meal_name
        INTEGER calories
        DECIMAL protein
        DECIMAL carbs
        DECIMAL fat
        VARCHAR image_url
        TIMESTAMP time
    }

    CHAT_HISTORIES {
        UUID id PK
        UUID user_id FK
        VARCHAR query
        VARCHAR response
        TIMESTAMP timestamp
    }

    NOTIFICATIONS {
        UUID id PK
        UUID user_id FK
        VARCHAR reminder_message
        VARCHAR schedule_cron
        BOOLEAN active
        TIMESTAMP last_sent
    }
```
