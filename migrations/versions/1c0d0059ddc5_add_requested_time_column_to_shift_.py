"""Add requested time column to shift report table.

Revision ID: 1c0d0059ddc5
Revises: 2c6f0b439301
Create Date: 2015-02-17 12:10:18.358081

"""

# revision identifiers, used by Alembic.
revision = '1c0d0059ddc5'
down_revision = '2c6f0b439301'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('shift_report', sa.Column('requested_time', sa.Float()))


def downgrade():
    op.drop_column('shift_report', 'requested_time')
