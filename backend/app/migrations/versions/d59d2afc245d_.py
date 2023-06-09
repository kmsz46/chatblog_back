"""empty message

Revision ID: d59d2afc245d
Revises: 7e3f03bd4463
Create Date: 2023-04-16 12:37:20.416718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd59d2afc245d'
down_revision = '7e3f03bd4463'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('threads',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=False),
    sa.Column('tag', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('sub_tag', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.String(length=255), nullable=True),
    sa.Column('group_op', sa.Boolean(), nullable=True),
    sa.Column('open_op', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usergroup',
    sa.Column('user_id', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'name')
    )
    op.create_table('responses',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('thread_id', sa.String(length=255), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('user_id', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['thread_id'], ['threads.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('threadgroup',
    sa.Column('thread_id', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['thread_id'], ['threads.id'], ),
    sa.PrimaryKeyConstraint('thread_id', 'name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('threadgroup')
    op.drop_table('responses')
    op.drop_table('usergroup')
    op.drop_table('threads')
    op.drop_table('users')
    # ### end Alembic commands ###
