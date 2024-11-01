"""add_created_at_for_record

Revision ID: a219db2bbb7f
Revises: bd2ec89f8994
Create Date: 2024-10-07 11:04:57.856595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a219db2bbb7f'
down_revision: Union[str, None] = 'bd2ec89f8994'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('record', sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False))


def downgrade() -> None:
    op.drop_column('record', 'created_at')
