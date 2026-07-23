import asyncio
import json
from datetime import datetime
from typing import Any

import structlog

from src.config.settings import settings
from src.services.ai.interfaces import LLMProvider

logger = structlog.get_logger()


class CircuitBreakerOpenError(Exception):
    """Exception raised when the circuit breaker is OPEN and fails fast."""

    pass


class CircuitBreaker:
    """Standard circuit breaker logic tracking consecutive errors count and tripping states."""

    def __init__(
        self, failure_threshold: int = 5, recovery_timeout_seconds: int = 30
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout_seconds
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.last_state_change = datetime.now()

    def record_success(self) -> None:
        """Resets consecutive failure counters."""
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self) -> None:
        """Increments fail count and trips state if threshold reached."""
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.last_state_change = datetime.now()
            logger.error(
                "Circuit breaker tripped to OPEN state",
                failure_count=self.failure_count,
            )

    def allow_request(self) -> bool:
        """Returns True if the request is permitted, False if tripped."""
        if self.state == "OPEN":
            # Check if recovery timeout has elapsed to enter HALF-OPEN
            elapsed = (datetime.now() - self.last_state_change).total_seconds()
            if elapsed > self.recovery_timeout:
                self.state = "HALF-OPEN"
                logger.info("Circuit breaker entering HALF-OPEN state for verification")
                return True
            return False
        return True


class GeminiProvider(LLMProvider):
    """Google Gemini AI service client wrapper with timeouts, retries, and circuit breakers."""

    def __init__(
        self,
        retries: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0,
        timeout: float = 15.0,
    ) -> None:
        self.retries = retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.timeout = timeout
        self.circuit_breaker = CircuitBreaker()
        self.api_key = settings.GEMINI_API_KEY
        self.is_mock = self.api_key == "dev_gemini_key"

        if not self.is_mock:
            try:
                import google.generativeai as genai

                genai.configure(api_key=self.api_key)
                self.client = genai
                logger.info("Gemini provider configured successfully.")
            except ImportError:
                logger.warning(
                    "google-generativeai SDK missing. Falling back to mock completion."
                )
                self.is_mock = True

    async def _execute_with_resilience(
        self, func: Any, *args: Any, **kwargs: Any
    ) -> Any:
        """Runs the query function wrapping retries, exponential backoffs, timeouts, and circuit breakers."""
        if not self.circuit_breaker.allow_request():
            logger.error("Circuit breaker is OPEN. Fast-failing Gemini API request.")
            raise CircuitBreakerOpenError("Gemini API circuit breaker is open.")

        delay = self.initial_delay
        for attempt in range(self.retries):
            try:
                # Timeout wrapped execution
                result = await asyncio.wait_for(
                    func(*args, **kwargs), timeout=self.timeout
                )
                self.circuit_breaker.record_success()
                return result
            except Exception as e:
                logger.warning(
                    "Gemini API request execution attempt failed",
                    attempt=attempt + 1,
                    error=str(e),
                )
                if attempt == self.retries - 1:
                    self.circuit_breaker.record_failure()
                    raise e
                await asyncio.sleep(delay)
                delay *= self.backoff_factor

    async def generate_response(
        self,
        system_prompt: str,
        prompt: str,
        history: list[dict[str, str]] | None = None,
        response_schema: Any | None = None,
    ) -> str:
        """Generates conversation completions from system prompts and inputs."""
        if self.is_mock:
            # Emulate structured JSON if schema requested
            if response_schema:
                # Default mock schemas responses
                return json.dumps(
                    {
                        "response": f"Mock response containing: '{prompt}'",
                        "calories": 230,
                        "protein": 10.0,
                        "carbs": 30.0,
                        "fat": 5.0,
                        "analysis": "Mock analysis content.",
                        "advice": "Keep up the great work!",
                        "safety": "safe",
                    }
                )
            return f"Mock answer to: '{prompt}' based on system: '{system_prompt}'"

        # Prepare payload logic with real SDK
        async def _call_gemini() -> str:
            model = self.client.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_prompt,
            )
            # Compile messages history if present
            contents = []
            if history:
                for h in history:
                    contents.append({"role": h["role"], "parts": [h["content"]]})
            contents.append({"role": "user", "parts": [prompt]})

            # Structured JSON settings config if requested
            config = {}
            if response_schema:
                config = {
                    "response_mime_type": "application/json",
                }

            # Run in executor because SDK calls are synchronous block calls
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None, lambda: model.generate_content(contents, generation_config=config)
            )
            return str(response.text)

        return str(await self._execute_with_resilience(_call_gemini))

    async def analyze_image(
        self,
        image_url_or_bytes: str | bytes,
        prompt: str,
        response_schema: Any | None = None,
    ) -> str:
        """Processes multimodal food image log descriptions."""
        if self.is_mock:
            # Return synthetic mock structure
            return json.dumps(
                {
                    "foods": ["Roti", "Paneer"],
                    "portions": ["2 pieces", "150g"],
                    "calories": 480,
                    "protein": 22.0,
                    "carbs": 55.0,
                    "fat": 15.0,
                    "confidence": 0.92,
                }
            )

        async def _call_gemini_multimodal() -> str:
            model = self.client.GenerativeModel(model_name="gemini-1.5-flash")

            # Prepare image payload
            image_part = {}
            if isinstance(image_url_or_bytes, bytes):
                image_part = {"mime_type": "image/jpeg", "data": image_url_or_bytes}
            else:
                # Fetch url image bytes first
                import httpx

                async with httpx.AsyncClient() as client:
                    resp = await client.get(image_url_or_bytes)
                    image_part = {"mime_type": "image/jpeg", "data": resp.content}

            contents = [image_part, prompt]
            config = {}
            if response_schema:
                config = {
                    "response_mime_type": "application/json",
                }

            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None, lambda: model.generate_content(contents, generation_config=config)
            )
            return str(response.text)

        return str(await self._execute_with_resilience(_call_gemini_multimodal))
