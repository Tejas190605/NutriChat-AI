# Functional Requirements Specification (functional_requirements.md)

This specification defines the functional features, requirements, user paths, and business rules for NutriChat AI.

---

## 1. User Onboarding & Profiles

### Requirements
*   **WhatsApp Intake Flow**: On receiving a message from an unregistered phone number, the chatbot must initiate the profile setup questionnaire.
*   **Parameters Collection**:
    1.  **Name**: Short string validation.
    2.  **Height (cm)**: Number range [100 - 250].
    3.  **Weight (kg)**: Number range [30 - 200].
    4.  **Goal**: Multi-choice selection: `Weight Loss`, `Muscle Gain`, `Maintain Weight`.
    5.  **Activity Level**: Selection: `Sedentary`, `Lightly Active`, `Moderately Active`, `Very Active`.
    6.  **Allergies / Preferences**: Text input (e.g. Vegetarian, Gluten-free, none).
*   **Daily Budget Calculation**:
    The system calculates the user's Total Daily Energy Expenditure (TDEE) using the Mifflin-St Jeor Formula:
    *   *Male*: $10 \times \text{weight} + 6.25 \times \text{height} - 5 \times \text{age} + 5$
    *   *Female*: $10 \times \text{weight} + 6.25 \times \text{height} - 5 \times \text{age} - 161$
    *   *Activity multiplier applied based on selection*.
    *   *Calorie Target adjusted by goal (e.g., -500 kcal for Weight Loss, +300 kcal for Muscle Gain).*

### Onboarding On-Demand Reset Flow
*   **Reset Directive**: At any point during the onboarding questionnaire, or at any time in the chat history, if the user sends `/reset`, the chatbot must:
    1.  Clear the active session onboarding state inside Redis.
    2.  Delete partially collected data caches.
    3.  Respond: *"Your onboarding details have been cleared. Let's start over! What is your name?"* and enter onboarding state again.

---

## 2. Multimodal Logging Intake

### Text Message Logging
*   *Action*: User sends text describing their meal (e.g. *"I ate 2 eggs and 1 slice of toast for breakfast"*).
*   *System Flow*: Parse quantity and food keywords, query Edamam API, store log, and return confirmation text.

### Voice Message Logging
*   *Action*: User sends a voice message recording.
*   *System Flow*: Transcribe WAV/AAC audio file to text using Whisper or Gemini API. Run parsed text through the standard text logging pipeline.

### Photo Message Logging
*   *Action*: User snaps a food photo.
*   *System Flow*: Vision AI detects dish types, portion volumes, and returns the analysis.

### Barcode Scan Logging
*   *Action*: User uploads a barcode picture.
*   *System Flow*: Detect barcode location, decode values, query Open Food Facts API, and log product macros.

---

## 3. Food Recognition, OCR, & Nutrition Calculation

### Image Classification Rules
*   **Indian Street & Traditional Food Support**: The system must accurately classify common dishes (e.g. Samosa, Chole Bhature, Dal Tadka, Butter Chicken, Dosa, Idli).
*   **Portion Size Detection**: Bounding shapes mapped to approximate quantities (e.g., `"2 pieces of Samosa"`, `"1 bowl of Dal"`, `"240g of Rice"`).
*   **OCR Parsing**: Read product label packages (ingredients, protein, fat, sodium levels) and log details to database.

---

## 4. Exercise & Activity Tracking

*   **Intake Commands**: Users can log exercises by texting details (e.g. *"I ran for 30 minutes"* or *"walked 10000 steps"*) or sending voice logs.
*   **MET-Based Calorie Deficit Calculations**: The system maps exercise categories to Metabolic Equivalent of Task (MET) codes:
    *   *Running*: 9.8 METs
    *   *Walking*: 3.8 METs
    *   *Cycling*: 7.5 METs
    *   *Calorie Deficit Formula*: $\text{Duration (mins)} \times \left(\text{MET} \times 3.5 \times \frac{\text{Weight (kg)}}{200}\right)$
*   **Net Calorie Adjustments**: Logged activities append to activity history tables and adjust the user's daily budget balance in real-time.

---

## 5. Conversational AI Coaching & Memory

### Memory Rules
*   Maintain conversational session context inside Redis (24-hour expiration).
*   Chat history must track queries, AI response scripts, and meal records.

### Alternative Food Suggestions
*   If a logged meal is high in fat or calories, the AI coach must suggest a healthier alternative.
    *   *Example*: User logs Chole Bhature (750 kcal). Coach replies: *"Chole Bhature is high in saturated fat. Next time, try a baked Dosa with coconut chutney (~280 kcal) for a lighter meal!"*

---

## 6. Daily, Weekly, & Monthly Reports
*   Provide a `/summary` command in WhatsApp returning:
    *   Remaining calorie allowance for the day.
    *   Target vs. logged macro-nutrients balance.
*   Dashboard Analytics exports weekly and monthly PDF report cards mapping target weight progress.

---

## 7. Webhook Payload Verification

*   **Signature Security Requirement**: To verify that inbound webhook POST payloads originate from Meta, the FastAPI backend must validate the `X-Hub-Signature-256` request header:
    *   *Algorithm*: HMAC-SHA256 signature generated over the raw request body bytes using the app's Facebook App Secret as the key.
    *   *Verification Flow*: Compare the generated hash with the header signature using constant-time comparison methods (`hmac.compare_digest`). Reject unauthorized payloads with HTTP 401.
