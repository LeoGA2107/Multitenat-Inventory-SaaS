"""change-on-the-table-users

Revision ID: 87afc3fead44
Revises: e973f8805c03
Create Date: 2026-10-08 14:55:15.072340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87afc3fead44'
down_revision: Union[str, Sequence[str], None] = 'e973f8805c03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'users', 
        'name', 
        new_column_name = 'username', 
        existing_type=sa.String(length=50))

    op.alter_column(
        'tenants',
        'name',
        new_column_name='tenantname',
        existing_type=sa.String(length=50)
    )
    

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'users',
        'username',
        new_column_name='name',
        existing_type=sa.String(length=50))

    op.alter_column(
        'tenants',
        'tenantname',
        new_column_name='name',
        existing_type=sa.String(length=50)
    )

    pass
