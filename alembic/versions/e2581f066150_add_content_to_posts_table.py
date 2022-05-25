"""add content to posts table

Revision ID: e2581f066150
Revises: f9c6d19b66ec
Create Date: 2022-05-25 13:55:02.899945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2581f066150'
down_revision = 'f9c6d19b66ec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
