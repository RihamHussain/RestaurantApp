"""rename customers table to users

Revision ID: 8d6f7fac6463
Revises: 6e8b574e82ca
Create Date: 2026-05-18 14:25:57.174498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d6f7fac6463'
down_revision: Union[str, Sequence[str], None] = '6e8b574e82ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.rename_table('customers', 'users')

def downgrade():
    op.rename_table('users', 'customers')