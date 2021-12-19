"""empty message

Revision ID: e38c28b18d0a
Revises: 
Create Date: 2021-12-18 16:26:56.588304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e38c28b18d0a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.Column('by', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('item_id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.Column('by', sa.String(length=50), nullable=True),
    sa.Column('parent', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['parent'], ['news.item_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('item_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('news')
    # ### end Alembic commands ###
