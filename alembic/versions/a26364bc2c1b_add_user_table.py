"""add user table

Revision ID: a26364bc2c1b
Revises: dc55c6904706
Create Date: 2023-02-20 17:53:34.977735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a26364bc2c1b'
down_revision = 'dc55c6904706'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )   
    pass


def downgrade():
    op.drop_table('users')
    pass
