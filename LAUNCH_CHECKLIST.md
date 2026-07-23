# Pre-Launch Verification Checklist (LAUNCH_CHECKLIST.md)

## 1. Environment & Infrastructure
- [x] SSL Certificates issued and active (HTTPS enforced).
- [x] Domain DNS records (A & CNAME) pointing to load balancer / NGINX reverse proxy.
- [x] Database migration `004_analytics_coaching_domain.py` applied cleanly.
- [x] Redis connection credentials & password authentication verified.

## 2. External Provider Integrations
- [x] Gemini API Key configured with quota tier active.
- [x] Meta WhatsApp Cloud API Webhook URL registered with `X-Hub-Signature-256` HMAC validation.
- [x] Cloudinary Storage API keys verified.

## 3. Security & Compliance Audit
- [x] All runtime Docker containers executing as non-root users (`appuser` / `nextjs`).
- [x] HTTP Security Headers verified (`HSTS`, `CSP`, `X-Frame-Options`, `X-Content-Type-Options`).
- [x] JWT Bearer Token secret minimum 64 characters long.

## 4. Frontend & PWA Verification
- [x] Web App Manifest (`manifest.ts`) returning valid JSON metadata.
- [x] Service Worker (`sw.js`) registered and pre-caching static assets.
- [x] 23/23 Next.js static pages prerendered with 0 TypeScript/ESLint errors.
