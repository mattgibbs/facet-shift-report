"""Add a string to keep the logbook entry url.

Revision ID: 33c1177d829a
Revises: 3a3c5a763cbe
Create Date: 2015-02-26 17:06:31.286466

"""

# revision identifiers, used by Alembic.
revision = '33c1177d829a'
down_revision = '3a3c5a763cbe'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('shift_report', sa.Column('logbook_entry_url', sa.String(140)))


def downgrade():
    op.drop_column('shift_report', 'logbook_entry_url')
