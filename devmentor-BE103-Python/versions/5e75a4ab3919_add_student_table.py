"""Add student table

Revision ID: 5e75a4ab3919
Revises: ff3c26ae043a
Create Date: 2024-08-05 14:06:21.190811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e75a4ab3919'
down_revision: Union[str, None] = 'ff3c26ae043a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "student",
        sa.Column("id", sa.Interval(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
    )
    pass


def downgrade() -> None:
    pass
