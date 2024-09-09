"""Add LINE user ID to User model

Revision ID: 42b2d91bbcb1
Revises: fdab6442de5f
Create Date: 2024-09-09 11:42:24.684683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42b2d91bbcb1'
down_revision: Union[str, None] = 'fdab6442de5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('line_user_id', sa.String(length=255), nullable=True))
    
    op.create_unique_constraint('uq_user_line_user_id', 'user', ['line_user_id'])
    
    op.alter_column('user', 'password',
               existing_type=sa.String(length=255),
               nullable=True)
    
    op.alter_column('user', 'username',
               existing_type=sa.String(length=255),
               nullable=True)


def downgrade() -> None:
    op.drop_constraint('uq_user_line_user_id', 'user', type_='unique')
    
    op.drop_column('user', 'line_user_id')
    
    op.alter_column('user', 'password',
               existing_type=sa.String(length=255),
               nullable=False)
    
    op.alter_column('user', 'username',
               existing_type=sa.String(length=255),
               nullable=False)
