"""Nutrition domain schema

Revision ID: 002_nutrition_domain
Revises: 001_initial_user_domain
Create Date: 2026-07-23 00:05:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '002_nutrition_domain'
down_revision: Union[str, None] = '001_initial_user_domain'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create food_categories table
    op.create_table(
        'food_categories',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_food_categories_name'), 'food_categories', ['name'], unique=True)

    # 2. Create nutrition_facts table
    op.create_table(
        'nutrition_facts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('calories', sa.Integer(), nullable=False),
        sa.Column('protein', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('carbs', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('fat', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('fiber', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('sugar', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('sodium', sa.Numeric(precision=7, scale=2), nullable=False),
        sa.Column('saturated_fat', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('serving_size', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('serving_unit', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 3. Create foods table
    op.create_table(
        'foods',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('category_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['food_categories.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_foods_name'), 'foods', ['name'], unique=True)

    # 4. Create ingredients table
    op.create_table(
        'ingredients',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_ingredients_name'), 'ingredients', ['name'], unique=True)

    # 5. Create food_ingredients association table
    op.create_table(
        'food_ingredients',
        sa.Column('food_id', sa.UUID(), nullable=False),
        sa.Column('ingredient_id', sa.UUID(), nullable=False),
        sa.Column('quantity', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('food_id', 'ingredient_id')
    )

    # 6. Create nutrition_profiles table
    op.create_table(
        'nutrition_profiles',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('food_id', sa.UUID(), nullable=True),
        sa.Column('ingredient_id', sa.UUID(), nullable=True),
        sa.Column('nutrition_fact_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['nutrition_fact_id'], ['nutrition_facts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('food_id'),
        sa.UniqueConstraint('ingredient_id')
    )

    # 7. Create meals table (supports soft delete)
    op.create_table(
        'meals',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('image_url', sa.String(length=512), nullable=True),
        sa.Column('logged_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_meals_user_logged'), 'meals', ['user_id', 'logged_at'], unique=False)

    # 8. Create meal_items table
    op.create_table(
        'meal_items',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('meal_id', sa.UUID(), nullable=False),
        sa.Column('food_id', sa.UUID(), nullable=True),
        sa.Column('food_name', sa.String(length=100), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('weight_grams', sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column('calories', sa.Integer(), nullable=False),
        sa.Column('protein', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('carbs', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('fat', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['meal_id'], ['meals.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_meal_items_meal'), 'meal_items', ['meal_id'], unique=False)

    # 9. Create barcode_products table
    op.create_table(
        'barcode_products',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('barcode', sa.String(length=50), nullable=False),
        sa.Column('product_name', sa.String(length=100), nullable=False),
        sa.Column('brand', sa.String(length=100), nullable=True),
        sa.Column('nutrition_fact_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['nutrition_fact_id'], ['nutrition_facts.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_barcode_products_barcode'), 'barcode_products', ['barcode'], unique=True)

    # 10. Create nutrition_labels table
    op.create_table(
        'nutrition_labels',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('raw_text', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(length=512), nullable=True),
        sa.Column('nutrition_fact_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['nutrition_fact_id'], ['nutrition_facts.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    # 11. Create restaurant_menus table
    op.create_table(
        'restaurant_menus',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('restaurant_name', sa.String(length=100), nullable=False),
        sa.Column('menu_item_name', sa.String(length=100), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('nutrition_fact_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['nutrition_fact_id'], ['nutrition_facts.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_restaurant_menus_restaurant_item'), 'restaurant_menus', ['restaurant_name', 'menu_item_name'], unique=False)

    # 12. Create grocery_products table
    op.create_table(
        'grocery_products',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('brand', sa.String(length=100), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('nutrition_fact_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['nutrition_fact_id'], ['nutrition_facts.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_grocery_products_name'), 'grocery_products', ['name'], unique=False)

    # 13. Create favorite_foods table
    op.create_table(
        'favorite_foods',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('food_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_favorite_foods_user'), 'favorite_foods', ['user_id'], unique=False)

    # 14. Create recent_foods table
    op.create_table(
        'recent_foods',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('food_id', sa.UUID(), nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('idx_recent_foods_user'), 'recent_foods', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_table('recent_foods')
    op.drop_table('favorite_foods')
    op.drop_index(op.f('idx_grocery_products_name'), table_name='grocery_products')
    op.drop_table('grocery_products')
    op.drop_index(op.f('idx_restaurant_menus_restaurant_item'), table_name='restaurant_menus')
    op.drop_table('restaurant_menus')
    op.drop_table('nutrition_labels')
    op.drop_index(op.f('idx_barcode_products_barcode'), table_name='barcode_products')
    op.drop_table('barcode_products')
    op.drop_index(op.f('idx_meal_items_meal'), table_name='meal_items')
    op.drop_table('meal_items')
    op.drop_index(op.f('idx_meals_user_logged'), table_name='meals')
    op.drop_table('meals')
    op.drop_table('nutrition_profiles')
    op.drop_table('food_ingredients')
    op.drop_index(op.f('idx_ingredients_name'), table_name='ingredients')
    op.drop_table('ingredients')
    op.drop_index(op.f('idx_foods_name'), table_name='foods')
    op.drop_table('foods')
    op.drop_table('nutrition_facts')
    op.drop_index(op.f('idx_food_categories_name'), table_name='food_categories')
    op.drop_table('food_categories')
