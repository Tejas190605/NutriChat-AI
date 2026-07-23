"""AI persistence domain

Revision ID: 003_ai_persistence_domain
Revises: 002_nutrition_domain
Create Date: 2026-07-23 00:10:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '003_ai_persistence_domain'
down_revision: Union[str, None] = '002_nutrition_domain'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create food_images table
    op.create_table(
        'food_images',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('image_url', sa.String(length=512), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_food_images_user'), 'food_images', ['user_id'], unique=False)
    op.create_index(op.f('idx_food_images_status'), 'food_images', ['status'], unique=False)
    op.create_index(op.f('idx_food_images_deleted'), 'food_images', ['deleted_at'], unique=False)

    # 2. Create ocr_results table
    op.create_table(
        'ocr_results',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('food_image_id', sa.UUID(), nullable=True),
        sa.Column('raw_text', sa.Text(), nullable=False),
        sa.Column('parsed_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['food_image_id'], ['food_images.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_ocr_results_image'), 'ocr_results', ['food_image_id'], unique=False)
    op.create_index(op.f('idx_ocr_results_deleted'), 'ocr_results', ['deleted_at'], unique=False)

    # 3. Create vision_predictions table
    op.create_table(
        'vision_predictions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('food_image_id', sa.UUID(), nullable=False),
        sa.Column('label', sa.String(length=100), nullable=False),
        sa.Column('confidence', sa.Numeric(precision=5, scale=4), nullable=False),
        sa.Column('box_coordinates', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['food_image_id'], ['food_images.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_vision_predictions_image'), 'vision_predictions', ['food_image_id'], unique=False)
    op.create_index(op.f('idx_vision_predictions_label'), 'vision_predictions', ['label'], unique=False)
    op.create_index(op.f('idx_vision_predictions_deleted'), 'vision_predictions', ['deleted_at'], unique=False)

    # 4. Create ai_conversations table
    op.create_table(
        'ai_conversations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_ai_conversations_user'), 'ai_conversations', ['user_id'], unique=False)
    op.create_index(op.f('idx_ai_conversations_active'), 'ai_conversations', ['is_active'], unique=False)
    op.create_index(op.f('idx_ai_conversations_deleted'), 'ai_conversations', ['deleted_at'], unique=False)

    # 5. Create ai_messages table
    op.create_table(
        'ai_messages',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('conversation_id', sa.UUID(), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tokens', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['ai_conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_ai_messages_conv'), 'ai_messages', ['conversation_id'], unique=False)
    op.create_index(op.f('idx_ai_messages_deleted'), 'ai_messages', ['deleted_at'], unique=False)

    # 6. Create prompt_templates table
    op.create_table(
        'prompt_templates',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_prompt_templates_name'), 'prompt_templates', ['name'], unique=True)
    op.create_index(op.f('idx_prompt_templates_deleted'), 'prompt_templates', ['deleted_at'], unique=False)

    # 7. Create prompt_versions table
    op.create_table(
        'prompt_versions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('template_id', sa.UUID(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('system_prompt', sa.Text(), nullable=False),
        sa.Column('user_prompt_template', sa.Text(), nullable=False),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('temperature', sa.Numeric(precision=3, scale=2), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['template_id'], ['prompt_templates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_prompt_versions_template'), 'prompt_versions', ['template_id'], unique=False)
    op.create_index(op.f('idx_prompt_versions_active'), 'prompt_versions', ['is_active'], unique=False)
    op.create_index(op.f('idx_prompt_versions_deleted'), 'prompt_versions', ['deleted_at'], unique=False)

    # 8. Create ai_requests table
    op.create_table(
        'ai_requests',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('prompt_version_id', sa.UUID(), nullable=True),
        sa.Column('request_payload', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['prompt_version_id'], ['prompt_versions.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_ai_requests_user'), 'ai_requests', ['user_id'], unique=False)
    op.create_index(op.f('idx_ai_requests_prompt'), 'ai_requests', ['prompt_version_id'], unique=False)
    op.create_index(op.f('idx_ai_requests_deleted'), 'ai_requests', ['deleted_at'], unique=False)

    # 9. Create ai_responses table
    op.create_table(
        'ai_responses',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('request_id', sa.UUID(), nullable=False),
        sa.Column('response_payload', sa.JSON(), nullable=False),
        sa.Column('latency_ms', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['request_id'], ['ai_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('request_id')
    )
    op.create_index(op.f('idx_ai_responses_request'), 'ai_responses', ['request_id'], unique=True)
    op.create_index(op.f('idx_ai_responses_deleted'), 'ai_responses', ['deleted_at'], unique=False)

    # 10. Create recommendations table
    op.create_table(
        'recommendations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_recommendations_user'), 'recommendations', ['user_id'], unique=False)
    op.create_index(op.f('idx_recommendations_category'), 'recommendations', ['category'], unique=False)
    op.create_index(op.f('idx_recommendations_deleted'), 'recommendations', ['deleted_at'], unique=False)

    # 11. Create recommendation_feedback table
    op.create_table(
        'recommendation_feedback',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('recommendation_id', sa.UUID(), nullable=False),
        sa.Column('feedback_value', sa.String(length=50), nullable=False),
        sa.Column('comments', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['recommendation_id'], ['recommendations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_rec_feedback_recommendation'), 'recommendation_feedback', ['recommendation_id'], unique=False)
    op.create_index(op.f('idx_rec_feedback_deleted'), 'recommendation_feedback', ['deleted_at'], unique=False)

    # 12. Create confidence_scores table
    op.create_table(
        'confidence_scores',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.UUID(), nullable=False),
        sa.Column('score', sa.Numeric(precision=5, scale=4), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_confidence_scores_type_id'), 'confidence_scores', ['entity_type', 'entity_id'], unique=False)
    op.create_index(op.f('idx_confidence_scores_deleted'), 'confidence_scores', ['deleted_at'], unique=False)

    # 13. Create token_usages table
    op.create_table(
        'token_usages',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('request_id', sa.UUID(), nullable=True),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('prompt_tokens', sa.Integer(), nullable=False),
        sa.Column('completion_tokens', sa.Integer(), nullable=False),
        sa.Column('total_tokens', sa.Integer(), nullable=False),
        sa.Column('cost', sa.Numeric(precision=10, scale=6), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['request_id'], ['ai_requests.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_token_usages_user'), 'token_usages', ['user_id'], unique=False)
    op.create_index(op.f('idx_token_usages_model'), 'token_usages', ['model_name'], unique=False)
    op.create_index(op.f('idx_token_usages_deleted'), 'token_usages', ['deleted_at'], unique=False)

    # 14. Create model_usages table
    op.create_table(
        'model_usages',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('call_count', sa.Integer(), nullable=False),
        sa.Column('total_prompt_tokens', sa.Integer(), nullable=False),
        sa.Column('total_completion_tokens', sa.Integer(), nullable=False),
        sa.Column('total_cost', sa.Numeric(precision=12, scale=6), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_model_usages_name'), 'model_usages', ['model_name'], unique=True)
    op.create_index(op.f('idx_model_usages_deleted'), 'model_usages', ['deleted_at'], unique=False)


def downgrade() -> None:
    op.drop_table('model_usages')
    op.drop_table('token_usages')
    op.drop_table('confidence_scores')
    op.drop_table('recommendation_feedback')
    op.drop_table('recommendations')
    op.drop_table('ai_responses')
    op.drop_table('ai_requests')
    op.drop_table('prompt_versions')
    op.drop_table('prompt_templates')
    op.drop_table('ai_messages')
    op.drop_table('ai_conversations')
    op.drop_table('vision_predictions')
    op.drop_table('ocr_results')
    op.drop_table('food_images')
