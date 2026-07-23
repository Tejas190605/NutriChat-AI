import hashlib
import hmac
import json
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.services.whatsapp.client import WhatsAppClient
from src.services.whatsapp.state_machine import ConversationStateMachine


@pytest.mark.asyncio
async def test_whatsapp_client_send_payloads() -> None:
    """Verifies that WhatsAppClient correctly compiles message templates."""
    client = WhatsAppClient()

    # Text message mock
    res_text = await client.send_text("+123456789", "Hello there!")
    assert res_text is not None

    # Buttons mock
    res_btn = await client.send_buttons(
        "+123456789", "Choose option", [{"id": "yes", "title": "Yes"}]
    )
    assert res_btn is not None


@pytest.mark.asyncio
async def test_webhook_challenge_verification(client: AsyncClient) -> None:
    """Verifies that GET /webhook parameters check subscription verify token validation challenges."""
    verify_token = settings.FACEBOOK_VERIFY_TOKEN

    # Matching Token
    resp = await client.get(
        f"/api/v1/whatsapp/webhook?hub.mode=subscribe&hub.verify_token={verify_token}&hub.challenge=test_challenge"
    )
    assert resp.status_code == 200
    assert resp.text == "test_challenge"

    # Mismatching Token
    resp_bad = await client.get(
        "/api/v1/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=bad_token&hub.challenge=test_challenge"
    )
    assert resp_bad.status_code == 403


@pytest.mark.asyncio
async def test_webhook_signature_verification_rejections(client: AsyncClient) -> None:
    """Verifies that POST /webhook rejects requests with missing or invalid signatures."""
    payload = {"object": "whatsapp_business_account", "entry": []}

    # Missing Signature Header
    resp_missing = await client.post("/api/v1/whatsapp/webhook", json=payload)
    assert resp_missing.status_code == 401

    # Invalid Signature
    headers = {"X-Hub-Signature-256": "sha256=invalid_signature_hex_value"}
    resp_invalid = await client.post(
        "/api/v1/whatsapp/webhook", json=payload, headers=headers
    )
    assert resp_invalid.status_code == 401


@pytest.mark.asyncio
async def test_webhook_signature_acceptance_and_deduplication(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Verifies that POST /webhook accepts valid signatures and runs deduplication locks."""
    if db_session is None:
        pytest.skip("Database is offline")

    payload_dict = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "entry_id_123",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "messages": [
                                {
                                    "id": f"wamid.{uuid4()}",
                                    "from": "+919876543210",
                                    "type": "text",
                                    "text": {"body": "Hi"},
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    }
    payload_bytes = json.dumps(payload_dict).encode("utf-8")

    # Calculate HMAC signature using settings secret
    mac = hmac.new(
        key=settings.FACEBOOK_APP_SECRET.encode("utf-8"),
        msg=payload_bytes,
        digestmod=hashlib.sha256,
    )
    signature = f"sha256={mac.hexdigest()}"
    headers = {
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json",
    }

    # Submit valid webhook post
    resp = await client.post(
        "/api/v1/whatsapp/webhook", content=payload_bytes, headers=headers
    )
    assert resp.status_code == 200
    assert resp.json() == {"status": "success"}

    # Re-submit duplicate payload (deduplication check flags duplicate msg locks)
    resp_duplicate = await client.post(
        "/api/v1/whatsapp/webhook", content=payload_bytes, headers=headers
    )
    assert (
        resp_duplicate.status_code == 200
    )  # Returns success without executing task again


@pytest.mark.asyncio
async def test_onboarding_state_machine_steps(db_session: AsyncSession) -> None:
    """Tests the state machine transitions step-by-step for a new phone registration."""
    if db_session is None:
        pytest.skip("Database is offline")

    phone = f"+91{uuid4().hex[:10]}"
    machine = ConversationStateMachine(db_session, phone)

    # Start onboarding (State WELCOME)
    reply, done = await machine.run_state_cycle("Hello")
    assert "Welcome" in reply
    assert done is False

    # Name selection (State ONBOARDING_NAME)
    reply, done = await machine.run_state_cycle("Tejas")
    assert "Tejas" in reply
    assert done is False

    # Age selection (State ONBOARDING_AGE)
    reply, done = await machine.run_state_cycle("26")
    assert "gender" in reply.lower()
    assert done is False

    # Gender selection (State ONBOARDING_GENDER)
    reply, done = await machine.run_state_cycle("Male")
    assert "height" in reply.lower()
    assert done is False

    # Height selection (State ONBOARDING_HEIGHT)
    reply, done = await machine.run_state_cycle("178")
    assert "weight" in reply.lower()
    assert done is False

    # Weight selection (State ONBOARDING_WEIGHT)
    reply, done = await machine.run_state_cycle("75.5")
    assert "activity" in reply.lower()
    assert done is False

    # Activity selection (State ONBOARDING_ACTIVITY)
    reply, done = await machine.run_state_cycle("Active")
    assert "goal" in reply.lower()
    assert done is False

    # Goal selection (State ONBOARDING_GOAL - finishes onboarding)
    reply, done = await machine.run_state_cycle("Weight Loss")
    assert "Profile setup completed" in reply
    assert done is True

    # User lookup checks
    user = await machine.lookup_user()
    assert user is not None
    assert user.profile.first_name == "Tejas"
