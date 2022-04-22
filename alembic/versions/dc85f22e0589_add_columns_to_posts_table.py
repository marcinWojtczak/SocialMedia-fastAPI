"""add columns to posts table

Revision ID: dc85f22e0589
Revises: 25ef3f415d21
Create Date: 2022-04-21 12:18:42.184840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc85f22e0589'
down_revision = '25ef3f415d21'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    pass
