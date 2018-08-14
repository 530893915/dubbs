"""empty message

Revision ID: 99a45d1f74c5
Revises: 845486662682
Create Date: 2018-08-07 22:15:32.718929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99a45d1f74c5'
down_revision = '845486662682'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('is_removed', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.String(length=100), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['front_user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'board', 'cms_user', ['author_id'], ['id'])
    op.create_foreign_key(None, 'cms_user_role', 'cms_user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'cms_user_role', 'cms_role', ['role_id'], ['id'])
    op.create_foreign_key(None, 'post', 'board', ['board_id'], ['id'])
    op.create_foreign_key(None, 'post', 'highlight_post', ['highlight_id'], ['id'])
    op.create_foreign_key(None, 'post', 'front_user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'cms_user_role', type_='foreignkey')
    op.drop_constraint(None, 'cms_user_role', type_='foreignkey')
    op.drop_constraint(None, 'board', type_='foreignkey')
    op.drop_table('comment')
    # ### end Alembic commands ###