"""Update DB name rent

Revision ID: a2ea91c97d13
Revises: 75635da4f8d8
Create Date: 2024-10-06 22:06:48.070613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2ea91c97d13'
down_revision = '75635da4f8d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rsync_job', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name_rent', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rsync_job', schema=None) as batch_op:
        batch_op.drop_column('name_rent')

    # ### end Alembic commands ###
