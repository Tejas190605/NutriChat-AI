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
