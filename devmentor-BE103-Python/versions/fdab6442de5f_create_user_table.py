"""create user table

Revision ID: fdab6442de5f
Revises: ff3c26ae043a
Create Date: 2024-08-08 11:16:04.664452

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdab6442de5f'
down_revision: Union[str, None] = 'ff3c26ae043a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("language", sa.String(length=50), nullable=False),
    )
    op.create_table(
        'event',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('route', sa.String(length=255), nullable=False),
        sa.Column('create_time', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('creator_id', sa.Integer, nullable=False),
    )
    op.create_table(
        'content',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('content', sa.String(length=255), nullable=False),
        sa.Column('event_id', sa.Integer, nullable=False),
        sa.Column('language', sa.String(length=50), nullable=False),
    )
    op.create_table(
        'event_user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('event_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('notifiy_time', sa.DateTime, nullable=True),
    )
    op.create_table(
        'record',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('action', sa.String(length=255), nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('event_id', sa.Integer, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table('user')
    op.drop_table('event')
    op.drop_table('content')
    op.drop_table('event_user')
    op.drop_table('record')
    pass
