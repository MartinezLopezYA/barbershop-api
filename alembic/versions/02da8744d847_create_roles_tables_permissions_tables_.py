"""Create roles tables, permissions tables and associations

Revision ID: 02da8744d847
Revises: c2d4c1591499
Create Date: 2025-03-30 00:50:33.618010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02da8744d847'
down_revision: Union[str, None] = 'c2d4c1591499'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
