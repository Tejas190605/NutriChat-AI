import hashlib
import hmac
import json
from typing import Any

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.db.session import get_async_session
from src.services.redis_client import get_redis_client
from src.services.whatsapp.router import WhatsAppRouter

logger = structlog.get_logger()
redis_client = get_redis_client()
router = APIRouter()


@router.get(
    "/webhook",
    response_class=Response,
    summary="Meta Webhook Verification GET challenge responder",
)
async def verify_webhook(
    request: Request,
) -> Response:
    """Verifies verify token parameter matching configurations, responding with the challenge text.

    Args:
        request: FastAPI HTTP request instance.

    Returns:
        HTTP Response containing challenge text string.
    """
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge", "")

    if mode == "subscribe" and token == settings.FACEBOOK_VERIFY_TOKEN:
        logger.info(
            "WhatsApp GET webhook verification challenge token matches configurations successfully"
        )
        return Response(content=challenge, media_type="text/plain")

    logger.warning(
        "WhatsApp GET webhook verification challenge mismatch errors", token=token
    )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Verification token mismatch",
    )


@router.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
    summary="Receives incoming WhatsApp message payload event updates",
)
async def receive_webhook(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    """Inspects X-Hub-Signature-256 header parameters and runs signature check, forwarding payload to dispatchers.

    Args:
        request: FastAPI HTTP request instance.
        db: Async database session.

    Returns:
        A dict confirmation response.
    """
    # 1. Signature Verification Check
    signature_header = request.headers.get("X-Hub-Signature-256", "")
    if not signature_header or not signature_header.startswith("sha256="):
        logger.warning("Missing or malformed X-Hub-Signature-256 header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature validation required",
        )

    expected_signature = signature_header.split("sha256=")[1]
    raw_body = await request.body()

    # Calculate HMAC SHA-256 digest
    mac = hmac.new(
        key=settings.FACEBOOK_APP_SECRET.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha256,
    )
    actual_signature = mac.hexdigest()

    if not hmac.compare_digest(expected_signature, actual_signature):
        logger.error(
            "WhatsApp webhook incoming POST signature verification mismatch",
            expected=expected_signature,
            actual=actual_signature,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature verification mismatch",
        )

    # 2. Parse JSON body payload and route tasks
    try:
        body = await request.json()
    except Exception as e:
        logger.error("Failed to parse incoming webhook body JSON data", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Malformed JSON body",
        ) from e

    # Log incoming payload event for admin metrics
    await redis_client.lpush("whatsapp_webhook_logs", raw_body.decode("utf-8"))
    await redis_client.ltrim("whatsapp_webhook_logs", 0, 99)  # Keep latest 100 entries

    whatsapp_router = WhatsAppRouter(db)
    await whatsapp_router.route_payload(body)

    return {"status": "success"}


@router.get(
    "/admin/health",
    status_code=status.HTTP_200_OK,
    summary="Fetch diagnostic log status of the Meta webhook channels",
)
async def webhook_health() -> dict[str, Any]:
    """Inspects recent webhook payload inputs.

    Returns:
        A dictionary with active metrics.
    """
    logs_raw = await redis_client.lrange("whatsapp_webhook_logs", 0, 9)
    logs = [log for log in logs_raw if log]
    return {
        "status": "healthy",
        "recent_payloads_received": len(logs),
        "payloads": logs,
    }


@router.get(
    "/admin/sessions",
    status_code=status.HTTP_200_OK,
    summary="List active onboarding sessions stored in Redis",
)
async def active_sessions() -> dict[str, Any]:
    """Scans Redis for active onboarding sessions keys.

    Returns:
        A dictionary listing active keys.
    """
    # Scan active whatsapp_session prefix keys
    keys = []
    cursor = 0
    while True:
        cursor, match_keys = await redis_client.scan(
            cursor=cursor, match="whatsapp_session:*"
        )
        keys.extend(match_keys)
        if cursor == 0:
            break

    sessions_list = []
    for key in keys:
        val = await redis_client.get(key)
        if val:
            try:
                sessions_list.append(json.loads(val))
            except Exception:
                sessions_list.append(val)

    return {
        "active_sessions_count": len(sessions_list),
        "sessions": sessions_list,
    }
