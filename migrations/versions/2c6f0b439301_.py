"""Add experiment title to user table.

Revision ID: 2c6f0b439301
Revises: 5388ecf1248d
Create Date: 2015-02-17 10:43:17.516812

"""

# revision identifiers, used by Alembic.
revision = '2c6f0b439301'
down_revision = '5388ecf1248d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('experiment_title', sa.String(length=140)))


def downgrade():
    op.drop_column('user', 'experiment_title')
