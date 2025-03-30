"""Create roles tables, permissions tables and associations

Revision ID: 872d82e21766
Revises: 02da8744d847
Create Date: 2025-03-30 00:54:52.992902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '872d82e21766'
down_revision: Union[str, None] = '02da8744d847'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
