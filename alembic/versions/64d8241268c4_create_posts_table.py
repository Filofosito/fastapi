"""create posts table

Revision ID: 64d8241268c4
Revises: 
Create Date: 2023-02-20 16:06:19.502904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64d8241268c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade(): 
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable =False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade(): 
    op.drop_table('posts')
    pass
