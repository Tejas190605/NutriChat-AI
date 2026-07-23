# Incident Response Matrix (INCIDENT_RESPONSE.md)

## Severity Levels

| Severity | Definition | Response SLA | Escalate To |
| :--- | :--- | :--- | :--- |
| **P1 - Critical** | Complete service outage or data breach | < 15 minutes | CTO / Lead DevOps |
| **P2 - High** | Primary feature down (e.g., Vision/OCR processing broken) | < 1 hour | Backend Lead |
| **P3 - Medium** | Non-critical bug (e.g., notification delay, minor UI overflow) | < 12 hours | Frontend Lead |
| **P4 - Low** | Minor cosmetic bug or documentation error | < 48 hours | On-call Engineer |

## Post-Mortem Requirement
A formal post-mortem must be conducted within 24 hours of resolving any P1 or P2 incident.
