"""Add a boolean column for hiding reports

Revision ID: 3a3c5a763cbe
Revises: 31e6983050db
Create Date: 2015-02-25 14:17:30.858190

"""

# revision identifiers, used by Alembic.
revision = '3a3c5a763cbe'
down_revision = '31e6983050db'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('shift_report', sa.Column('hidden', sa.Boolean(), default=False))

def downgrade():
    op.drop_column('shift_report', 'hidden')
