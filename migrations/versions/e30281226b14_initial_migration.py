"""Initial migration.

Revision ID: e30281226b14
Revises: 
Create Date: 2022-11-05 08:21:03.329445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e30281226b14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('startJob', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('finishJob', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'finishJob')
    op.drop_column('user', 'startJob')
    # ### end Alembic commands ###