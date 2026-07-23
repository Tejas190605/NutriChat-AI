# API Reference (API_REFERENCE.md)

This catalog details the backend API routes, payloads, and response payloads.

---

## 1. Authentication Routes

### Register User Dashboard Access
*   **Route**: `POST /api/v1/auth/register`
*   **Description**: Register a new admin user for the dashboard panel.
*   **Request Headers**: `Content-Type: application/json`
*   **Request Body**:
    ```json
    {
      "email": "admin@nutrichat.ai",
      "password": "SecurePassword123"
    }
    ```
*   **Responses**:
    *   **201 Created**:
        ```json
        {
          "status": "success",
          "message": "User registered successfully",
          "user_id": "8f3b610c-9a4f-4d37-83b6-2856db326554"
        }
        ```
    *   **400 Bad Request** (Email already exists, password weak).

### Login User Dashboard Access
*   **Route**: `POST /api/v1/auth/login`
*   **Description**: Login and obtain a JWT access token.
*   **Request Body**:
    ```json
    {
      "email": "admin@nutrichat.ai",
      "password": "SecurePassword123"
    }
    ```
*   **Responses**:
    *   **200 OK**:
        ```json
        {
          "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
          "token_type": "bearer"
        }
        ```
    *   **401 Unauthorized** (Invalid email or password).

---

## 2. WhatsApp Webhook Routes

### Verify Webhook Token
*   **Route**: `GET /api/v1/webhook`
*   **Description**: Meta WhatsApp API webhook verification check.
*   **Query Parameters**:
    *   `hub.mode`: string (should equal `subscribe`)
    *   `hub.challenge`: string
    *   `hub.verify_token`: string
*   **Responses**:
    *   **200 OK**: Plaintext response returning the value of `hub.challenge`.
    *   **403 Forbidden** (Token mismatch).

### Process Incoming WhatsApp Message Events
*   **Route**: `POST /api/v1/webhook`
*   **Description**: Process inbound texts, audio logs, and image URLs.
*   **Request Body**:
    ```json
    {
      "object": "whatsapp_business_account",
      "entry": [
        {
          "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
          "changes": [
            {
              "value": {
                "messaging_product": "whatsapp",
                "metadata": {
                  "display_phone_number": "PHONE_NUMBER",
                  "phone_number_id": "PHONE_NUMBER_ID"
                },
                "contacts": [
                  {
                    "profile": { "name": "Tejas" },
                    "wa_id": "1234567890"
                  }
                ],
                "messages": [
                  {
                    "from": "1234567890",
                    "id": "wamid.HBgLMTIzNDU2Nzg5MFVVAAYg...",
                    "timestamp": "1721669812",
                    "type": "text",
                    "text": { "body": "How many calories in an apple?" }
                  }
                ]
              },
              "field": "messages"
            }
          ]
        }
      ]
    }
    ```
*   **Responses**:
    *   **200 OK**:
        ```json
        {
          "status": "processed",
          "message_id": "wamid.HBgLMTIzNDU2Nzg5MFVVAAYg..."
        }
        ```

---

## 3. Meal Logs Routes

### Retrieve User Meals
*   **Route**: `GET /api/v1/meals`
*   **Description**: Fetch daily logs. Requires JWT authorization header.
*   **Headers**: `Authorization: Bearer <token>`
*   **Query Parameters**:
    *   `date`: YYYY-MM-DD (Defaults to current local date).
*   **Responses**:
    *   **200 OK**:
        ```json
        [
          {
            "id": "23fa3b45-12e3-4f99-8877-ab3b6e82ef10",
            "meal_name": "Paneer Roti and Salad",
            "calories": 480,
            "protein": 22.5,
            "carbs": 55.0,
            "fat": 15.2,
            "timestamp": "2026-07-22T14:30:00Z"
          }
        ]
        ```

### Log Meal Entry Manually
*   **Route**: `POST /api/v1/meals/log`
*   **Description**: Log a food item manually.
*   **Headers**: `Authorization: Bearer <token>`
*   **Request Body**:
    ```json
    {
      "meal_name": "Banana",
      "calories": 105,
      "protein": 1.3,
      "carbs": 27.0,
      "fat": 0.3
    }
    ```
*   **Responses**:
    *   **201 Created**:
        ```json
        {
          "status": "success",
          "meal_id": "99f3c10a-8a4f-4d37-83b6-2856db326577"
        }
        ```

---

## 4. AI Persistence Routes

All AI persistence routes require JWT authorization `Authorization: Bearer <token>`.

### Start a Conversation Session
*   **Route**: `POST /api/v1/ai/conversations`
*   **Description**: Starts a new AI conversation session thread tracker.
*   **Request Body**:
    ```json
    {
      "title": "Onboarding Coaching"
    }
    ```
*   **Responses**:
    *   **201 Created**: Returns the conversation response.

### List Conversations
*   **Route**: `GET /api/v1/ai/conversations`
*   **Description**: Returns active conversation threads logged for the current user.
*   **Responses**:
    *   **200 OK**: List of active conversation metadata objects.

### Retrieve Conversation Details & Message History
*   **Route**: `GET /api/v1/ai/conversations/{conversation_id}`
*   **Description**: Returns messages history list within a conversation thread context.
*   **Responses**:
    *   **200 OK**: Full details dictionary including messages list arrays.

### Append a Message
*   **Route**: `POST /api/v1/ai/conversations/{conversation_id}/messages`
*   **Description**: Logs a user/assistant reply to the thread history.
*   **Request Body**:
    ```json
    {
      "role": "user",
      "content": "Need customized target deficit suggestions",
      "tokens": 15
    }
    ```
*   **Responses**:
    *   **201 Created**: Returns message details response.

### Update Conversation Title or Status
*   **Route**: `PUT /api/v1/ai/conversations/{conversation_id}`
*   **Description**: Updates title or closes active conversation logs.
*   **Request Body**:
    ```json
    {
      "title": "New Title",
      "is_active": false
    }
    ```
*   **Responses**:
    *   **200 OK**: Returns updated conversation response.

### Delete Conversation
*   **Route**: `DELETE /api/v1/ai/conversations/{conversation_id}`
*   **Description**: Soft deletes conversation session history records.
*   **Responses**:
    *   **204 No Content**

### Create Prompt Template Header
*   **Route**: `POST /api/v1/ai/prompts/templates`
*   **Description**: Registers a prompt category identifier.
*   **Request Body**:
    ```json
    {
      "name": "coaching_agent",
      "description": "Standard prompt template rules"
    }
    ```
*   **Responses**:
    *   **201 Created**: Returns prompt template header response.

### Create Prompt Version
*   **Route**: `POST /api/v1/ai/prompts/templates/{template_id}/versions`
*   **Description**: Pushes template formatting guidelines version.
*   **Request Body**:
    ```json
    {
      "version": 1,
      "system_prompt": "You are a health coach.",
      "user_prompt_template": "Analyze: {food}",
      "model_name": "gemini-1.5-flash",
      "temperature": 0.5,
      "is_active": true
    }
    ```
*   **Responses**:
    *   **201 Created**: Returns prompt version template response.

### Fetch Active Prompt Version Config
*   **Route**: `GET /api/v1/ai/prompts/templates/{name}/active`
*   **Description**: Returns active guidelines prompt instructions config.
*   **Responses**:
    *   **200 OK**: Active prompt version response.

### Log a Recommendation
*   **Route**: `POST /api/v1/ai/recommendations`
*   **Description**: Logs recommendation suggestions generated.
*   **Request Body**:
    ```json
    {
      "category": "alternative",
      "content": {"swap": "brown rice"}
    }
    ```
*   **Responses**:
    *   **201 Created**

### Log Recommendation Feedback
*   **Route**: `POST /api/v1/ai/recommendations/{recommendation_id}/feedback`
*   **Description**: Logs ratings feedback for a swap recommendation.
*   **Request Body**:
    ```json
    {
      "feedback_value": "liked",
      "comments": "Great swap advice!"
    }
    ```
*   **Responses**:
    *   **201 Created**

---

## 5. Computer Vision Routes

### Upload Food Image and Process
*   **Route**: `POST /api/v1/vision/upload`
*   **Description**: Accepts multipart image file, resizes it using Pillow, uploads it to Cloudinary/local fallback, creates a database log, and dispatches background processing tasks. Requires JWT authorization.
*   **Request Headers**: `Authorization: Bearer <token>`, `Content-Type: multipart/form-data`
*   **Request Body**:
    *   `file`: Binary image file (multipart/form-data)
*   **Responses**:
    *   **201 Created**:
        ```json
        {
          "status": "success",
          "message": "Image uploaded successfully. Background processing started.",
          "image_id": "4da67eb5-12e3-4f99-8877-ab3b6e82ef22",
          "image_url": "http://localhost:8000/static/uploads/4da67eb5-12e3-4f99-8877-ab3b6e82ef22.jpg",
          "image_status": "uploaded"
        }
        ```


