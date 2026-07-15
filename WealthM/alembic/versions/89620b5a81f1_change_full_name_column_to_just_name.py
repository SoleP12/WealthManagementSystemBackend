"""Change full_name column to just name

Revision ID: 89620b5a81f1
Revises: 60c281448c84
Create Date: 2026-07-11 12:34:29.462956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89620b5a81f1'
down_revision: Union[str, Sequence[str], None] = '60c281448c84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'full_name', new_column_name='name', existing_type=sa.String(), existing_nullable=True)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
