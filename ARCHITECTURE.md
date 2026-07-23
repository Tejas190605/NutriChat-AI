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
        Auth --> SignatureVerify[HMAC-SHA256 Signature Verify]
        SignatureVerify --> Caching{Redis Deduplication}
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
    Meta->>Webhook: Webhook Payload (HTTP POST with X-Hub-Signature-256)
    Webhook->>Webhook: Validate HMAC-SHA256 signature using APP_SECRET
    alt Signature Mismatch
        Webhook-->>Meta: 401 Unauthorized
    else Signature Valid
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
    end
```

---

## 3. Conversational State Machine (Onboarding & Reset Flow)

When an incoming message event is delivered, the backend checks the user's registration status. Below is the state machine representation of the onboarding flow, including the on-demand `/reset` trigger:

```mermaid
stateDiagram-v2
    [*] --> CheckRegistration
    CheckRegistration --> Onboarding_Start : User not found
    CheckRegistration --> ActiveTracking : User exists
    
    state Onboarding_Start {
        [*] --> AskName
        AskName --> AskHeight : Name received
        AskHeight --> AskWeight : Height valid
        AskWeight --> AskGoal : Weight valid
        AskGoal --> AskActivity : Goal valid
        AskActivity --> SetTargets : Activity valid
        SetTargets --> ProfileComplete
        
        AskName --> OnboardingReset : User sends "/reset"
        AskHeight --> OnboardingReset : User sends "/reset"
        AskWeight --> OnboardingReset : User sends "/reset"
        AskGoal --> OnboardingReset : User sends "/reset"
        AskActivity --> OnboardingReset : User sends "/reset"
        
        OnboardingReset --> AskName : Session Cleared
    }
    
    ProfileComplete --> ActiveTracking : Onboarding completed
    
    state ActiveTracking {
        [*] --> ParseInput
        ParseInput --> TextPipeline : Input is Text
        ParseInput --> VoicePipeline : Input is Audio
        ParseInput --> VisionPipeline : Input is Image/Photo
        ParseInput --> BarcodePipeline : Input is Barcode
        ParseInput --> ResetTracking : User sends "/reset"
        
        TextPipeline --> SaveLog
        VoicePipeline --> SaveLog
        VisionPipeline --> SaveLog
        BarcodePipeline --> SaveLog
        
        SaveLog --> SuggestAlternatives
        SuggestAlternatives --> [*]
        
        ResetTracking --> Onboarding_Start : Session Cleared
    }
```

---

## 4. Database ERD (Entity Relationship Diagram)

Includes the added `user_activities` table mapping exercise logs and MET-based calculations.

```mermaid
erDiagram
    USERS ||--o{ MEALS : "logs"
    USERS ||--o{ CHAT_HISTORIES : "stores"
    USERS ||--o{ NOTIFICATIONS : "manages"
    USERS ||--o{ USER_ACTIVITIES : "performs"
    USERS ||--o{ FOOD_IMAGES : "uploads"
    USERS ||--o{ AI_CONVERSATIONS : "starts"
    USERS ||--o{ RECOMMENDATIONS : "receives"
    FOOD_IMAGES ||--o{ OCR_RESULTS : "parses"
    FOOD_IMAGES ||--o{ VISION_PREDICTIONS : "classifies"
    AI_CONVERSATIONS ||--o{ AI_MESSAGES : "contains"
    PROMPT_TEMPLATES ||--o{ PROMPT_VERSIONS : "versions"
    PROMPT_VERSIONS ||--o{ AI_REQUESTS : "formats"
    AI_REQUESTS ||--o| AI_RESPONSES : "resolves"
    AI_REQUESTS ||--o{ TOKEN_USAGES : "measures"
    RECOMMENDATIONS ||--o{ RECOMMENDATION_FEEDBACK : "collects"

    USERS {
        UUID id PK
        VARCHAR name
        DECIMAL height
        DECIMAL weight
        VARCHAR goal
        VARCHAR activity_level
        INTEGER target_calories
        DECIMAL target_protein
        DECIMAL target_carbs
        DECIMAL target_fat
        TIMESTAMP created_at
    }

    MEALS {
        UUID id PK
        UUID whatsapp_user_id FK
        VARCHAR meal_name
        INTEGER calories
        DECIMAL protein
        DECIMAL carbs
        DECIMAL fat
        VARCHAR quantity
        VARCHAR image_url
        TIMESTAMP time
    }

    CHAT_HISTORIES {
        UUID id PK
        UUID whatsapp_user_id FK
        VARCHAR role
        VARCHAR message_body
        TIMESTAMP timestamp
    }

    NOTIFICATIONS {
        UUID id PK
        UUID whatsapp_user_id FK
        VARCHAR reminder_message
        VARCHAR schedule_cron
        BOOLEAN active
        TIMESTAMP last_sent
    }

    USER_ACTIVITIES {
        UUID id PK
        UUID whatsapp_user_id FK
        VARCHAR activity_name
        DECIMAL duration_minutes
        DECIMAL MET_value
        INTEGER calories_burned
        TIMESTAMP time
    }

    FOOD_IMAGES {
        UUID id PK
        UUID user_id FK
        VARCHAR image_url
        VARCHAR status
        TIMESTAMP created_at
    }

    OCR_RESULTS {
        UUID id PK
        UUID food_image_id FK
        TEXT raw_text
        JSON parsed_json
        TIMESTAMP created_at
    }

    VISION_PREDICTIONS {
        UUID id PK
        UUID food_image_id FK
        VARCHAR label
        DECIMAL confidence
        JSON box_coordinates
        TIMESTAMP created_at
    }

    AI_CONVERSATIONS {
        UUID id PK
        UUID user_id FK
        VARCHAR title
        BOOLEAN is_active
        TIMESTAMP created_at
    }

    AI_MESSAGES {
        UUID id PK
        UUID conversation_id FK
        VARCHAR role
        TEXT content
        INTEGER tokens
        TIMESTAMP created_at
    }

    PROMPT_TEMPLATES {
        UUID id PK
        VARCHAR name
        VARCHAR description
        TIMESTAMP created_at
    }

    PROMPT_VERSIONS {
        UUID id PK
        UUID template_id FK
        INTEGER version
        TEXT system_prompt
        TEXT user_prompt_template
        VARCHAR model_name
        DECIMAL temperature
        BOOLEAN is_active
        TIMESTAMP created_at
    }

    AI_REQUESTS {
        UUID id PK
        UUID user_id FK
        UUID prompt_version_id FK
        JSON request_payload
        TIMESTAMP created_at
    }

    AI_RESPONSES {
        UUID id PK
        UUID request_id FK
        JSON response_payload
        INTEGER latency_ms
        TIMESTAMP created_at
    }

    RECOMMENDATIONS {
        UUID id PK
        UUID user_id FK
        VARCHAR category
        JSON content
        TIMESTAMP created_at
    }

    RECOMMENDATION_FEEDBACK {
        UUID id PK
        UUID recommendation_id FK
        VARCHAR feedback_value
        VARCHAR comments
        TIMESTAMP created_at
    }

```


---

## 5. Computer Vision & OCR Upload Pipeline Sequence

Below is the execution flow of the Image Preprocessing, Cloudinary upload, and Celery background task:

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as FastAPI Upload Route
    participant Pre as Image Preprocessing (Pillow)
    participant Storage as Cloudinary / Local Storage
    participant DB as PostgreSQL
    participant Task as Celery Worker
    participant Cache as Redis

    Client->>API: Upload Multipart File (meal.png)
    API->>Pre: Resize (max 800x800) & Compress (quality 85)
    Pre-->>API: Return Compressed JPEG Bytes
    API->>Storage: Upload Image Bytes
    Storage-->>API: Return Secure Image URL
    API->>DB: Log FoodImage (status: "uploaded")
    API->>Task: Dispatch Background task (delay)
    API-->>Client: Return 201 Created (image_id, url)
    
    Task->>DB: Update FoodImage (status: "processing")
    Task->>Cache: Query cached predictions for URL
    alt Cache Hit
        Cache-->>Task: Return Cached Results
    else Cache Miss
        Task->>Task: Run Vision & OCR Mock providers
        Task->>Cache: Set cache results (TTL 24 hours)
    end
    Task->>DB: Log VisionPredictions & OCRResults
    Task->>DB: Update FoodImage (status: "completed")
```

---

## 6. Architectural Quality Standards

*   **DRY & Repository Pattern**: All database queries must inherit from a base repository class to avoid repeating SQLAlchemy connection logic.
*   **Asynchronous-First**: Route controllers leverage asynchronous databases routines to prevent blocking the worker event loops during heavy concurrent read operations.
*   **Decoupled AI Engine**: Prompt orchestration classes are isolated from route logic. Changing the underlying vision AI client (e.g. switching from Gemini to OpenAI) requires no modifications to webhook routes.
