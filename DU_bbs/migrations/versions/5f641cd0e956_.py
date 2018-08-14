"""empty message

Revision ID: 5f641cd0e956
Revises: 66fc052cf8f1
Create Date: 2018-07-28 20:02:54.740568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f641cd0e956'
down_revision = '66fc052cf8f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cms_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('desc', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('permission', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cms_role')
    # ### end Alembic commands ###
