"""add position field for user

Revision ID: 349077407852
Revises: 039457afd4b0
Create Date: 2023-11-10 19:18:55.223277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '349077407852'
down_revision: Union[str, None] = '039457afd4b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('position', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'position')
    # ### end Alembic commands ###