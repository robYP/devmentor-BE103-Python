"""Add ON DELETE SET NULL to user_id and event_id in Record

Revision ID: a652f9167dbe
Revises: fdab6442de5f
Create Date: 2024-08-20 09:35:15.160262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a652f9167dbe'
down_revision: Union[str, None] = 'fdab6442de5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('record_ibfk_1', 'record', type_='foreignkey')
    op.drop_constraint('record_ibfk_2', 'record', type_='foreignkey')
    
    op.create_foreign_key(
        'record_ibfk_1',  
        'record', 'user', 
        ['user_id'], ['id'],
        ondelete='SET NULL'
    )
    op.create_foreign_key(
        'record_ibfk_2',
        'record', 'event',
        ['event_id'], ['id'],
        ondelete='SET NULL'
    )
    pass


def downgrade() -> None:
    op.drop_constraint('record_ibfk_1', 'record', type_='foreignkey')
    op.drop_constraint('record_ibfk_2', 'record', type_='foreignkey')
    
    op.create_foreign_key(
        'record_ibfk_1', 
        'record', 'user',
        ['user_id'], ['id'],
        ondelete=None
    )
    op.create_foreign_key(
        'record_ibfk_2',
        'record', 'event',
        ['event_id'], ['id'],
        ondelete=None
    )
    pass
