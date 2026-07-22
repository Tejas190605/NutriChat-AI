# User Journeys & Flows (flows.md)

This document charts the user onboarding, meal tracking flows, information architecture, and site hierarchies for NutriChat AI.

---

## 1. User Journeys (Persona: weight-loss enthusiast)

*   **Goal**: Log daily caloric intake on WhatsApp with minimal frictional load, monitor weekly deficits, and track active metrics.
*   **Onboarding Steps**:
    1.  User sends a greeting (e.g. *"Hi"*) to the NutriChat AI WhatsApp number.
    2.  Chatbot identifies the user is untracked and begins asking for name, height, weight, activity multiplier, and goal target.
    3.  User answers each question sequentially.
    4.  System confirms calculation: *"Profile complete, Tejas! Your calculated daily target is 1,850 kcal. Send me any food photo or text to start tracking!"*
*   **Active Tracking Steps**:
    1.  User takes a picture of their breakfast plate (Scrambled eggs and coffee) and sends it.
    2.  System processes the image and responds with a breakdown: *"Logged Scrambled Eggs (2 eggs, 180 kcal) and Black Coffee (0 kcal). Remaining: 1,670 kcal."*
    3.  User goes to the Admin Dashboard (if authorized) to review their logged logs charts and weight tracking meters.

---

## 2. Information Architecture (IA)

NutriChat AI separates features into WhatsApp interactions (for the end-user) and Web-based layouts (for administrators).

```
[NutriChat AI Core IA]
 ├── Client Intake (WhatsApp Chatbot)
 │    ├── Profile Setup Questionnaire
 │    ├── Multimodal Intake Webhook (Image, Audio, Barcode, Text)
 │    ├── Feedback Confirmations
 │    └── Active Coaching Q&A
 │
 └── System Administration (Web Dashboard)
      ├── Landing Page (Sign up, Pricing details, Core Features)
      ├── Dashboard (Active Users, DB stats, API status logs)
      ├── User logs Overview (Daily Active Users, Meal logs history)
      ├── Settings & Security Rules configuration
      └── Feedback Audit logs
```

---

## 3. Web Dashboard Navigation Map & Page Hierarchy

Below is the layout routing structure for the Admin Panel:

*   **`/`**: Landing Page (Publicly accessible, contains signup triggers).
*   **`/auth/login` & `/auth/register`**: Dashboard security gates.
*   **`/dashboard`**: Unified Overview Panel.
    *   **`/dashboard/users`**: User list, active profiles, parameters history.
    *   **`/dashboard/meals`**: Historical meals index logs.
    *   **`/dashboard/analytics`**: Real-time stats (Calorie trends, popular items, API hit costs).
    *   **`/dashboard/settings`**: System configurations, cache flushes, profile limits.
    *   **`/dashboard/feedback`**: User feedback records review.
*   **`/404` / `/500`**: Custom error layouts.
