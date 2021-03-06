"""empty message

Revision ID: 63e630b29712
Revises: 84b96e8a6b3e
Create Date: 2018-08-10 16:44:27.287374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63e630b29712'
down_revision = '84b96e8a6b3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'board', 'cms_user', ['author_id'], ['id'])
    op.create_foreign_key(None, 'cms_user_role', 'cms_role', ['role_id'], ['id'])
    op.create_foreign_key(None, 'cms_user_role', 'cms_user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'comment', ['origin_comment_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'post', ['post_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'front_user', ['author_id'], ['id'])
    op.add_column('front_user', sa.Column('avatar', sa.String(length=100), nullable=True))
    op.add_column('front_user', sa.Column('old_login_time', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'post', 'board', ['board_id'], ['id'])
    op.create_foreign_key(None, 'post', 'front_user', ['author_id'], ['id'])
    op.create_foreign_key(None, 'post', 'highlight_post', ['highlight_id'], ['id'])
    op.create_foreign_key(None, 'post_star', 'front_user', ['author_id'], ['id'])
    op.create_foreign_key(None, 'post_star', 'post', ['post_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post_star', type_='foreignkey')
    op.drop_constraint(None, 'post_star', type_='foreignkey')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('front_user', 'old_login_time')
    op.drop_column('front_user', 'avatar')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'cms_user_role', type_='foreignkey')
    op.drop_constraint(None, 'cms_user_role', type_='foreignkey')
    op.drop_constraint(None, 'board', type_='foreignkey')
    # ### end Alembic commands ###
