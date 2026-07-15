"""added total_assets and total_debt

Revision ID: 41db1775701b
Revises: 89620b5a81f1
Create Date: 2026-07-11 16:43:16.560965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41db1775701b'
down_revision: Union[str, Sequence[str], None] = '89620b5a81f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
