# Architectural Decision Records (DECISIONS.md)

This log tracks critical design and architectural selections made throughout the development of NutriChat AI.

---

## ADR 001: Technical Stack and Integration Framework
*   **Status**: Approved
*   **Date**: 2026-07-22

### Problem
We need to design a backend and conversational application layer that can support:
1. Low latency response generation for text/voice queries.
2. Large binary intake processing (photos/audio voice clips).
3. Highly modular AI vision and OCR routines.
4. Seamless integration with WhatsApp.

### Alternatives
*   **Option A: Node.js (Express/NestJS)**
    *   *Pros*: Fast event loops, rich ecosystem for webhooks.
    *   *Cons*: Python integration for machine learning/AI clients (Gemini API, OCR, portion calculations) requires spawning sub-processes or separate microservices, adding latency and complexity.
*   **Option B: Python (FastAPI) [Selected]**
    *   *Pros*: Native async support, high performance (Uvicorn), direct integration with Python AI/ML libraries, automatic OpenAPI schema generation, simple database ORM tools (SQLAlchemy).
    *   *Cons*: Slightly lower raw throughput compared to Node.js/Go, but completely negligible relative to AI model API call latency.

### Decision
Utilize **Python FastAPI** as the primary backend engine.

### Reasoning
Since NutriChat AI's core functionality relies heavily on processing images, extracting nutrition data via LLMs/Vision APIs, and handling voice recordings, having a single high-performance Python environment simplifies execution, reduces deployment complexity, and allows developers to write async processing flows natively.

### Tradeoffs
*   Requires managing async library structures carefully (e.g. databases must support async drivers).
*   FastAPI requires uvicorn processes, needing careful multi-process configuration in Docker containers.

### Impact
*   Boilerplate folders mapped to Python packages.
*   All web server, client wrappers (Edamam, Open Food Facts), and ML engines written in Python.

### Future Considerations
If the Admin Dashboard requires heavy socket interactions, a separate Node.js server might be evaluated, but FastAPI's native WebSocket support should suffice.
