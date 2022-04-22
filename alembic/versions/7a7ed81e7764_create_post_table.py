"""create post table

Revision ID: 7a7ed81e7764
Revises: 
Create Date: 2022-04-20 20:06:20.620305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a7ed81e7764'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                             sa.Column("title", sa.String(), nullable=False),
                             sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
