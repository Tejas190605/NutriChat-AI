"""Celery Application Compatibility Module.

Note: NutriChat AI is optimized for 100% Render Free deployment using direct asynchronous request execution.
Celery worker dependencies are disabled in this tier.
"""

from typing import Any, Callable


class DummyCeleryApp:
    """Lightweight stub replacing Celery app instance in synchronous Free Tier mode."""

    def task(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            return func

        return decorator


celery_app = DummyCeleryApp()
