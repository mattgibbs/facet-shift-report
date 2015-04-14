"""Add sigma columns for beam parameters

Revision ID: 526fe2c96c87
Revises: 28c3cf129d69
Create Date: 2015-04-14 11:20:42.093612

"""

# revision identifiers, used by Alembic.
revision = '526fe2c96c87'
down_revision = '28c3cf129d69'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shift_report', sa.Column('bunch_length_sigma', sa.Float(), nullable=True))
    op.add_column('shift_report', sa.Column('numParticles_sigma', sa.Float(), nullable=True))
    op.add_column('shift_report', sa.Column('x_rms_li20_sigma', sa.Float(), nullable=True))
    op.add_column('shift_report', sa.Column('y_rms_li20_sigma', sa.Float(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shift_report', 'y_rms_li20_sigma')
    op.drop_column('shift_report', 'x_rms_li20_sigma')
    op.drop_column('shift_report', 'numParticles_sigma')
    op.drop_column('shift_report', 'bunch_length_sigma')
    ### end Alembic commands ###