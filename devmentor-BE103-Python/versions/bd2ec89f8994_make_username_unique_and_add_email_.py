"""Make username unique and add email column

Revision ID: bd2ec89f8994
Revises: 42b2d91bbcb1
Create Date: 2024-09-30 11:17:53.335519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd2ec89f8994'
down_revision: Union[str, None] = '42b2d91bbcb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make username unique
    op.create_unique_constraint('uq_user_username', 'user', ['username'])
    
    # Add email column
    op.add_column('user', sa.Column('email', sa.String(length=255), nullable=True))


def downgrade() -> None:
    # Remove email column
    op.drop_column('user', 'email')
    
    # Remove unique constraint from username
    op.drop_constraint('uq_user_username', 'user', type_='unique')
