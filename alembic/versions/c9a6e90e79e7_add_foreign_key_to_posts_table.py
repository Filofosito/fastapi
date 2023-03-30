"""add foreign-key to posts table

Revision ID: c9a6e90e79e7
Revises: a26364bc2c1b
Create Date: 2023-02-20 18:09:11.553458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9a6e90e79e7'
down_revision = 'a26364bc2c1b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable= False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraing('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
