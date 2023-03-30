"""add last few columns to posts

Revision ID: 2d16f268aecc
Revises: c9a6e90e79e7
Create Date: 2023-02-20 18:24:28.436189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d16f268aecc'
down_revision = 'c9a6e90e79e7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column(
        'published', sa.Boolean(), nullable =False, server_default = 'TRUE'),)
    op.add_column('posts', sa.Column(  
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

    pass
