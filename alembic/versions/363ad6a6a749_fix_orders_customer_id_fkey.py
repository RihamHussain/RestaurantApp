"""fix_orders_customer_id_fkey

Revision ID: 363ad6a6a749
Revises: 8d6f7fac6463
Create Date: 2026-05-21 14:43:40.932838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '363ad6a6a749'
down_revision: Union[str, Sequence[str], None] = '8d6f7fac6463'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint(
        'orders_customer_id_fkey',   # old constraint name
        'orders',
        type_='foreignkey'
    )
    op.create_foreign_key(
        'orders_customer_id_fkey',   # new constraint name
        'orders',                    # source table
        'users',                     # target table  ← this is the fix
        ['customer_id'],             # source column
        ['id'],                      # target column
        ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint(
        'orders_customer_id_fkey',
        'orders',
        type_='foreignkey'
    )
    op.create_foreign_key(
        'orders_customer_id_fkey',
        'orders',
        'customers',                 # reverts back to old table
        ['customer_id'],
        ['id'],
        ondelete='CASCADE'
    )