"""empty message

Revision ID: a223b4fdc7e4
Revises: 99a45d1f74c5
Create Date: 2018-08-08 10:15:23.741528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a223b4fdc7e4'
down_revision = '99a45d1f74c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'board', 'cms_user', ['author_id'], ['id'])
    op.create_foreign_key(None, 'cms_user_role', 'cms_role', ['role_id'], ['id'])
    op.create_foreign_key(None, 'cms_user_role', 'cms_user', ['user_id'], ['id'])
    op.add_column('comment', sa.Column('origin_comment_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comment', 'comment', ['origin_comment_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'front_user', ['author_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'post', ['post_id'], ['id'])
    op.create_foreign_key(None, 'post', 'highlight_post', ['highlight_id'], ['id'])
    op.create_foreign_key(None, 'post', 'board', ['board_id'], ['id'])
    op.create_foreign_key(None, 'post', 'front_user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_column('comment', 'origin_comment_id')
    op.drop_constraint(None, 'cms_user_role', type_='foreignkey')
    op.drop_constraint(None, 'cms_user_role', type_='foreignkey')
    op.drop_constraint(None, 'board', type_='foreignkey')
    # ### end Alembic commands ###
