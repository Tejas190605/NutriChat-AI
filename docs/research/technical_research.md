# Technical Research Report: APIs, Frameworks, & Patterns (technical_research.md)

This report details the background technical research completed during Phase 1 of the NutriChat AI project lifecycle.

---

## 1. AI Models & Multimodal Inference Pipeline

### Gemini 2.5
*   **Context Window**: 1,000,000+ tokens, allowing extensive chat history contexts.
*   **Capabilities**: Native support for image (multimodal) and audio inputs. This allows us to feed WhatsApp image downloads or voice notes (WAV/AAC) directly to the model API for parsing, bypassing separate transcription steps if latency targets are satisfied.
*   **Latency Profile**: Processing images takes 2s to 4s.

### OpenAI Vision (Fallback Model)
*   **Model**: `gpt-4o` or similar vision models.
*   **Role**: Used when the Gemini API encounters transient timeouts, quota exhaustion, or safety block alerts.
*   **Fallback Trigger logic**:
    ```python
    try:
        response = call_gemini_vision_api(image_bytes)
    except APIError as e:
        logger.warning("Gemini Vision failed, falling back to OpenAI: %s", e)
        response = call_openai_vision_api(image_bytes)
    ```

---

## 2. External API Integrations

### WhatsApp Cloud API
*   **Webhook Handshake**: Requires handling a `GET` handshake request from Meta containing verification parameters (`hub.mode`, `hub.challenge`, and `hub.verify_token`).
*   **Payload Intake**: Inbound messages are delivered as `POST` JSON payloads. Media items (images, audio) do not contain raw binary contents; instead, they provide a `media_id` which must be resolved to a download URL via:
    `GET https://graph.facebook.com/v18.0/<MEDIA_ID>`
    followed by fetching the binary stream with the authorization header:
    `Authorization: Bearer <WHATSAPP_ACCESS_TOKEN>`.
*   **Expiration**: Media download URLs expire after **5 minutes**.

### Edamam Nutrition & Food Database API
*   **Endpoints**:
    *   `POST /api/food-database/v2/nutrients`: For querying detailed calories, protein, fat, and carb summaries based on parsed food names and quantities.
*   **Rate Limits**: Free tier allows 5 requests per minute.
*   **Caching Strategy**: Every unique parsed ingredient (e.g. `"1 apple"`, `"2 roti"`) must be stored in PostgreSQL and cached in Redis.

### Open Food Facts API
*   **Endpoint**: `GET https://world.openfoodfacts.org/api/v0/product/<BARCODE>.json`
*   **Utility**: Returns structured JSON containing ingredients, brand name, nutritional profiles, and Nutri-Score grades.
*   **Rate limits**: Very lenient, but caching barcode mappings is standard practice.

---

## 3. Backend Architecture Standards (FastAPI & Celery)

*   **Asynchronous Database Connections**: Use SQLAlchemy's async connection engine (`create_async_engine`) with `asyncpg` drivers.
*   **Asynchronous Tasks (Celery + Redis)**: Since resolving WhatsApp image links, sending them to Vision LLMs, and performing Edamam queries can exceed standard HTTP timeout limits (e.g., 10 seconds), the incoming WhatsApp webhook must acknowledge the request immediately (return 200 OK within 2 seconds) and dispatch the heavy processing to Celery background workers:
    ```python
    @app.post("/api/v1/webhook")
    async def receive_webhook(payload: dict, background_tasks: BackgroundTasks):
        # Dispatch to Celery background task
        process_whatsapp_message.delay(payload)
        return {"status": "accepted"}
    ```
*   **Dependency Injection**: Use FastAPI dependencies to inject asynchronous db sessions (`get_async_session`) and authenticated users context.

---

## 4. Frontend Architecture Standards (Next.js 14 App Router)

*   **Server vs. Client Components**: Place data fetching queries in Server Components (fetching data directly from FastAPI backend) to reduce bundle size. Interactive elements (charts, tables, settings forms) are marked with `'use client'`.
*   **CSS Styling**: Use Tailwind CSS variables. Integrate Shadcn UI components for charts and analytics tables.
*   **Uptime Monitoring**: Dashboard calls a `/api/v1/health` endpoint periodically to inspect database, Redis, and API client connection status.

---

## 5. PostgreSQL Schema & Index Design

*   **Foreign Keys**: Explicit indexing on `user_id` across `meals` and `chat_histories` tables to prevent slow query execution times as user records grow.
*   **Indices**:
    *   Composite index on `(user_id, time DESC)` for the `meals` table to speed up Daily/Weekly reporting views.
    *   Unique index on `user_id` inside profiles table.
