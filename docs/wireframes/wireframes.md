# Screen Wireframes (wireframes.md)

This catalog details ASCII wireframes for all 17 screens and layout views required for NutriChat AI.

---

## 1. Landing Page

```
+-----------------------------------------------------------------------------+
|  [Logo] NutriChat AI                      Features   Pricing   [Get Started] |
+-----------------------------------------------------------------------------+
|                                                                             |
|            Track Calories on WhatsApp With a Simple Food Photo              |
|                                                                             |
|         No manual logging. Take a picture, send, get instant analysis.      |
|                                                                             |
|                                [Start Free Now]                             |
|                                                                             |
|             +-------------------------------------------------+             |
|             | [Image: Smartphone rendering WhatsApp Chat]     |             |
|             |                                                 |             |
|             | User: [Photo of Samosa]                         |             |
|             | Chatbot: "Samosa (1 piece - 260 kcal).          |             |
|             |           Remaining: 1540 kcal."                |             |
|             +-------------------------------------------------+             |
|                                                                             |
+-----------------------------------------------------------------------------+
|  MIT License © 2026 NutriChat AI                          [GitHub] [Privacy] |
+-----------------------------------------------------------------------------+
```

---

## 2. Authentication (Login & Register)

```
+-----------------------------------------------------------------------------+
|                                                                             |
|                                NutriChat AI                                 |
|                                                                             |
|                          +-----------------------+                          |
|                          |     Sign In Admin     |                          |
|                          |                       |                          |
|                          | Email Address         |                          |
|                          | [                     ]                          |
|                          |                       |                          |
|                          | Password              |                          |
|                          | [                     ]                          |
|                          |                       |                          |
|                          |       [Login]         |                          |
|                          +-----------------------+                          |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 3. Onboarding Questionnaire (WhatsApp Mockup)

```
+-----------------------------------------------------------------------------+
|                                                                             |
|   +---------------------------------------------------------------------+   |
|   | NutriChat AI Chatbot                                                |   |
|   +---------------------------------------------------------------------+   |
|   | Chatbot: "Welcome to NutriChat AI! Let's get to know you.           |   |
|   |           What is your name?"                                       |   |
|   | User: "Tejas"                                                       |   |
|   | Chatbot: "Nice to meet you Tejas! What is your height in cm?"       |   |
|   | User: "180"                                                         |   |
|   | Chatbot: "Great. What is your current weight in kg?"                |   |
|   | User: "75"                                                          |   |
|   | Chatbot: "Understood. What is your goal? Reply with weight loss,    |   |
|   |           muscle gain, or maintain weight."                         |   |
|   | User: "weight loss"                                                 |   |
|   | Chatbot: "Calculated daily limit: 1850 kcal. Profile complete!"     |   |
|   +---------------------------------------------------------------------+   |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 4. Main Admin Dashboard Panel

```
+-----------------------------------------------------------------------------+
|  [Sidebar]  |  [Header] Users: 1,240  | Active: 840  | Health: 99.9%         |
|  Overview   +---------------------------------------------------------------+
|  Users      |                                                               |
|  Meals      |   [KPI Card 1]          [KPI Card 2]          [KPI Card 3]    |
|  Analytics  |   Daily Active Users    Meals Logged Today    API Latency     |
|  Feedback   |   840 (+12%)            3,240                 340ms           |
|  Settings   |                                                               |
|             |   +-------------------------------------------------------+   |
|             |   | Calorie Logging Activity History (Chart)              |   |
|             |   |                                                       |   |
|             |   |  * * *                                                |   |
|             |   | *     * * *                                           |   |
|             |   |            * *                                        |   |
|             |   +-------------------------------------------------------+   |
|             |                                                               |
+-------------+---------------------------------------------------------------+
```

---

## 5. User Profiles Management (Admin View)

```
+-----------------------------------------------------------------------------+
|  [Sidebar]  |  Search: [ Enter Name... ]                         [+ Add User]|
|             +---------------------------------------------------------------+
|             |  ID      | Name    | Weight | Goal        | Created At        |
|             | ---------|---------|--------|-------------|-------------------|
|             |  usr_01  | Tejas   | 75kg   | Weight Loss | 2026-07-22        |
|             |  usr_02  | Rahul   | 88kg   | Muscle Gain | 2026-07-20        |
|             |                                                               |
+-------------+---------------------------------------------------------------+
```

---

## 6. Meal Logs History Table

```
+-----------------------------------------------------------------------------+
|  [Sidebar]  |  Meal Logs History                                            |
|             +---------------------------------------------------------------+
|             |  User  | Meal Name           | Calories | Macros             |
|             | -------|---------------------|----------|--------------------|
|             | Tejas  | Samosa (1 piece)    | 260 kcal | P: 4g C: 32g F: 12g|
|             | Rahul  | Chicken Rice (150g) | 420 kcal | P: 35g C: 45g F: 8g|
|             |                                                               |
+-------------+---------------------------------------------------------------+
```

---

## 7. AI Chat Testing Sandbox Panel

```
+-----------------------------------------------------------------------------+
|  [Sidebar]  |  AI Chat Sandbox Testing                                      |
|             +---------------------------------------------------------------+
|             |  System Prompts Selector: [ Default Health Coach v1 ]         |
|             |  +---------------------------------------------------------+  |
|             |  | Chatbot: "How can I assist your health targets today?"  |  |
|             |  | User: "Can I eat banana for dinner?"                    |  |
|             |  | Chatbot: "Yes, bananas are rich in potassium. However..."|  |
|             |  +---------------------------------------------------------+  |
|             |  Input message: [                                ]  [Send]    |
|             +---------------------------------------------------------------+
```

---

## 8. Dashboard Analytics & Reports Chart

```
+-----------------------------------------------------------------------------+
|  [Sidebar]  |  Nutrition Analytics Reports                       [Export PDF]|
|             +---------------------------------------------------------------+
|             |  User: [ Tejas           ]    Date Range: [ Last 7 Days       ] |
|             |                                                               |
|             |   +-------------------------------------------------------+   |
|             |   | Caloric Targets vs. Intake History (Bar Chart)        |   |
|             |   |                                                       |   |
|             |   |   Log   Target                                        |   |
|             |   |   [x]    [ ]  1850 kcal                               |   |
|             |   |   [x]    [ ]  1700 kcal                               |   |
|             |   +-------------------------------------------------------+   |
|             |                                                               |
+-------------+---------------------------------------------------------------+
```

---

## 9. System Config Settings

```
+-----------------------------------------------------------------------------+
|  [Sidebar]  |  Settings Settings                                           |
|             +---------------------------------------------------------------+
|             |  Rate Limiting Rules Configuration                           |
|             |  Webhook Max Hits/Sec: [ 5 ]                                  |
|             |                                                               |
|             |  External Credentials Configuration                           |
|             |  Gemini API Key: [ ************************ ]                 |
|             |                                                               |
|             |  [Save Changes]                              [Flush Caches]   |
|             +---------------------------------------------------------------+
```

---

## 10. System Active Health Check logs

```
+-----------------------------------------------------------------------------+
|  [Sidebar]  |  System Status Check Logs                                     |
|             +---------------------------------------------------------------+
|             |  PostgreSQL Database:    ✅ Connected (12ms latency)           |
|             |  Redis Cache:            ✅ Running (2ms latency)             |
|             |  WhatsApp Webhook API:   ✅ OK (200 status returned)           |
|             |  Edamam Nutrition API:   ✅ Running (280ms API response time) |
|             |                                                               |
|             |  [Run Diagnostic Checks Now]                                 |
|             +---------------------------------------------------------------+
```

---

## 11. Custom Error Pages (e.g. 404 Layout)

```
+-----------------------------------------------------------------------------+
|                                                                             |
|                                NutriChat AI                                 |
|                                                                             |
|                                    404                                      |
|                                                                             |
|                           Page Could Not Be Found                           |
|                                                                             |
|                The link is broken or the page does not exist.               |
|                                                                             |
|                             [Back to Dashboard]                             |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 12. Empty States Views (e.g. Meals History Empty)

```
+-----------------------------------------------------------------------------+
|  [Sidebar]  |  Meal Logs History                                            |
|             +---------------------------------------------------------------+
|             |                                                               |
|             |                     No Meals Logged Today                     |
|             |                                                               |
|             |       You haven't logged any meals on WhatsApp today.         |
|             |       Send a photo or text to start calorie recording!        |
|             |                                                               |
+-------------+---------------------------------------------------------------+
```

---

## 13. Loading States Indicator

```
+-----------------------------------------------------------------------------+
|  [Sidebar]  |  Fetching Analytics...                                        |
|             +---------------------------------------------------------------+
|             |                                                               |
|             |                           Loading                             |
|             |                                                               |
|             |                      [ Spinning Ring ]                        |
|             |                                                               |
+-------------+---------------------------------------------------------------+
```
