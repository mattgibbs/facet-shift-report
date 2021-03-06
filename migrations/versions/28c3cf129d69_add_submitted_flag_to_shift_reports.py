"""Add submitted flag to shift reports.

Revision ID: 28c3cf129d69
Revises: 25d9a35ebe74
Create Date: 2015-03-25 09:51:03.704944

"""

# revision identifiers, used by Alembic.
revision = '28c3cf129d69'
down_revision = '25d9a35ebe74'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shift_report', sa.Column('submitted', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shift_report', 'submitted')
    ### end Alembic commands ###
