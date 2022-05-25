"""add last few columns to posts

Revision ID: b7c472f8c822
Revises: bde3aaf66cdc
Create Date: 2022-05-25 14:21:48.643394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7c472f8c822'
down_revision = 'bde3aaf66cdc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))

    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
