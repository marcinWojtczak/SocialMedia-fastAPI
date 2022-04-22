"""add published column

Revision ID: daa289e62239
Revises: 7a7ed81e7764
Create Date: 2022-04-20 20:48:32.978775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daa289e62239'
down_revision = '7a7ed81e7764'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean, server_default="TRUE", nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    pass
