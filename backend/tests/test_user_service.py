import pytest
from uuid import uuid4
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.user_service import UserService
from src.schemas.profile import UserProfileUpdateRequest


@pytest.mark.asyncio
async def test_user_profile_management(db_session: AsyncSession) -> None:
    """Verifies profile creation, retrieve, and updates."""
    if db_session is None:
        pytest.skip("Database is offline")
        
    user_id = uuid4()
    user_service = UserService(db_session)

    # Retrieves empty default profile
    profile = await user_service.get_profile(user_id)
    assert profile.user_id == user_id
    assert profile.first_name is None

    # Update profile
    update_data = UserProfileUpdateRequest(
        first_name="Tejas",
        last_name="Sabnis",
        gender="male",
        height=175.0,
        weight=75.0,
        date_of_birth=date(1995, 1, 1),
    )
    updated = await user_service.update_profile(user_id, update_data)
    assert updated.first_name == "Tejas"
    assert float(updated.height) == 175.0
    assert float(updated.weight) == 75.0

    # Ensure weight entry is logged in weight history
    history = await user_service.get_weight_history(user_id)
    assert len(history) == 1
    assert float(history[0].weight) == 75.0


@pytest.mark.asyncio
async def test_goal_calculation_formula(db_session: AsyncSession) -> None:
    """Verifies MSJ formula calculations for active goals."""
    if db_session is None:
        pytest.skip("Database is offline")
        
    user_id = uuid4()
    user_service = UserService(db_session)

    # Configure profile parameters
    update_data = UserProfileUpdateRequest(
        gender="male",
        height=180.0,
        weight=80.0,
        date_of_birth=date(2000, 1, 1),
    )
    await user_service.update_profile(user_id, update_data)

    # Target: Weight Loss
    goal = await user_service.calculate_and_save_goals(
        user_id, goal_type="weight_loss", activity_multiplier=1.375
    )
    assert goal.goal_type == "weight_loss"
    assert goal.is_active is True
    
    # Check calorie calculations
    assert goal.target_calories is not None
    assert 1950 <= goal.target_calories <= 2000

    # Check protein macros split (80kg * 2 = 160g)
    assert float(goal.target_protein) == 160.0

    # Target: Muscle Gain (should create a new active goal and deactivate the previous one)
    new_goal = await user_service.calculate_and_save_goals(
        user_id, goal_type="muscle_gain", activity_multiplier=1.2
    )
    assert new_goal.goal_type == "muscle_gain"
    assert new_goal.is_active is True

    # Check that previous goal is now deactivated
    active_goal = await user_service.get_active_goal(user_id)
    assert active_goal is not None
    assert active_goal.id == new_goal.id
