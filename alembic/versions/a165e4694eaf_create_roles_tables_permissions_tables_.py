"""Create roles tables, permissions tables and associations

Revision ID: a165e4694eaf
Revises: 872d82e21766
Create Date: 2025-03-30 09:52:09.634364

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a165e4694eaf'
down_revision: Union[str, None] = '872d82e21766'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
