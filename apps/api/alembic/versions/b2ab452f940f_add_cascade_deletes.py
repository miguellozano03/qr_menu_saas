"""add cascade deletes

Revision ID: b2ab452f940f
Revises: 92b9b13ba9f1
Create Date: 2026-04-15 09:57:23.183271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2ab452f940f'
down_revision: Union[str, Sequence[str], None] = '92b9b13ba9f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('categories_restaurant_id_fkey', 'categories', type_='foreignkey')
    op.create_foreign_key('categories_restaurant_id_fkey', 'categories', 'restaurants', ['restaurant_id'], ['id'], ondelete='CASCADE')

    op.drop_constraint('products_restaurant_id_fkey', 'products', type_='foreignkey')
    op.drop_constraint('products_category_id_fkey', 'products', type_='foreignkey')
    op.create_foreign_key('products_restaurant_id_fkey', 'products', 'restaurants', ['restaurant_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('products_category_id_fkey', 'products', 'categories', ['category_id'], ['id'], ondelete='CASCADE')

    op.drop_constraint('restaurant_links_restaurant_id_fkey', 'restaurant_links', type_='foreignkey')
    op.create_foreign_key('restaurant_links_restaurant_id_fkey', 'restaurant_links', 'restaurants', ['restaurant_id'], ['id'], ondelete='CASCADE')

    op.drop_constraint('restaurants_owner_id_fkey', 'restaurants', type_='foreignkey')
    op.create_foreign_key('restaurants_owner_id_fkey', 'restaurants', 'users', ['owner_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('products_restaurant_id_fkey', 'products', type_='foreignkey')
    op.drop_constraint('products_category_id_fkey', 'products', type_='foreignkey')
    op.create_foreign_key('products_restaurant_id_fkey', 'products', 'restaurants', ['restaurant_id'], ['id'])
    op.create_foreign_key('products_category_id_fkey', 'products', 'categories', ['category_id'], ['id'])

    op.drop_constraint('restaurant_links_restaurant_id_fkey', 'restaurant_links', type_='foreignkey')
    op.create_foreign_key('restaurant_links_restaurant_id_fkey', 'restaurant_links', 'restaurants', ['restaurant_id'], ['id'])

    op.drop_constraint('categories_restaurant_id_fkey', 'categories', type_='foreignkey')
    op.create_foreign_key('categories_restaurant_id_fkey', 'categories', 'restaurants', ['restaurant_id'], ['id'])

    op.drop_constraint('restaurants_owner_id_fkey', 'restaurants', type_='foreignkey')
    op.create_foreign_key('restaurants_owner_id_fkey', 'restaurants', 'users', ['owner_id'], ['id'])
