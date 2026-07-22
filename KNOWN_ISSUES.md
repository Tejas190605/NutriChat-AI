# Known Issues (KNOWN_ISSUES.md)

This log tracks unresolved bugs, limitations, and temporary workarounds for NutriChat AI.

---

## 1. Active Bugs
*No active bugs have been reported. Development has not yet commenced.*

---

## 2. Platform & System Limitations

### Issue L-01: WhatsApp Webhook Payload Media URL Expirations
*   **Description**: Meta WhatsApp API returns media URLs (images and audio clips) that expire after 5 minutes.
*   **Workaround**: Download raw media streams immediately upon receiving webhook POST payloads, and store them securely in our Cloudinary storage bucket. Do not persist Meta media URL paths directly in the database.

### Issue L-02: Edamam Free Tier API Rate Limits
*   **Description**: Edamam free tier permits only 5 requests per minute.
*   **Workaround**: Standardize caching logic on Redis. For any unrecognized foods, query and cache their macros permanently. Map identical food keywords locally before invoking the Edamam endpoint.
