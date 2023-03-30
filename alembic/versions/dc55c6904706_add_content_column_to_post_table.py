"""add content column to post table

Revision ID: dc55c6904706
Revises: 64d8241268c4
Create Date: 2023-02-20 17:44:56.564059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc55c6904706'
down_revision = '64d8241268c4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content', sa.String(), nullable =False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
