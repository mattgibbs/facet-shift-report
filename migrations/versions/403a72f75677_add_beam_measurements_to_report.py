"""Add beam measurements to report.

Revision ID: 403a72f75677
Revises: 33c1177d829a
Create Date: 2015-03-23 10:07:11.677627

"""

# revision identifiers, used by Alembic.
revision = '403a72f75677'
down_revision = '33c1177d829a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shift_report', sa.Column('bunch_length', sa.Float(), nullable=True))
    op.add_column('shift_report', sa.Column('numParticles', sa.Float(), nullable=True))
    op.add_column('shift_report', sa.Column('usesPositrons', sa.Boolean(), nullable=True, default=False))
    op.add_column('shift_report', sa.Column('x_emittance_li20', sa.Float(), nullable=True))
    op.add_column('shift_report', sa.Column('y_emittance_li20', sa.Float(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shift_report', 'y_emittance_li20')
    op.drop_column('shift_report', 'x_emittance_li20')
    op.drop_column('shift_report', 'usesPositrons')
    op.drop_column('shift_report', 'numParticles')
    op.drop_column('shift_report', 'bunch_length')
    ### end Alembic commands ###
