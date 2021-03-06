"""empty message

Revision ID: 7c598bc472f0
Revises: 5f641cd0e956
Create Date: 2018-07-28 20:07:32.481556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c598bc472f0'
down_revision = '5f641cd0e956'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cms_user_role',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['cms_role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['cms_user.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cms_user_role')
    # ### end Alembic commands ###
