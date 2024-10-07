"""add_event_name_for_record

Revision ID: 08f7b57cdefe
Revises: a219db2bbb7f
Create Date: 2024-10-07 23:24:03.622022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08f7b57cdefe'
down_revision: Union[str, None] = 'a219db2bbb7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('record', sa.Column('event_name', sa.String(length=255), nullable=False))


def downgrade() -> None:
    op.drop_column('record', 'event_name')
