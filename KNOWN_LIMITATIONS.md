# System Capacity & Known Limitations (KNOWN_LIMITATIONS.md)

## Operational Boundaries (v1.0 Release)
1. **WhatsApp Cloud API Rate Limit**: Meta API limits outbound messaging to 80 messages/sec per phone number.
2. **Food Image Recognition**: Recognition accuracy is highest for standard Indian dishes (88%+ accuracy); mixed buffet plates may have a ±15% calorie margin of error.
3. **Offline Queue Capacity**: IndexedDB offline queue holds up to 100 pending meal entries per client before requiring network replay.
4. **Celery Worker Concurrency**: Default worker concurrency is configured to 4 parallel processing threads per container.
