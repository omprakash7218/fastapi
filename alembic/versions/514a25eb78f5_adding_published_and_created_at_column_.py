"""adding published and created at column into posts table

Revision ID: 514a25eb78f5
Revises: 88236ed6425d
Create Date: 2026-06-12 16:35:09.984993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '514a25eb78f5'
down_revision = '88236ed6425d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='True'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
