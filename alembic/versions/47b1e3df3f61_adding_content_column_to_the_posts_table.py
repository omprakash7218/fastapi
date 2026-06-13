"""adding content column to the posts table

Revision ID: 47b1e3df3f61
Revises: 68ad0dadaafd
Create Date: 2026-06-12 15:34:28.655204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47b1e3df3f61'
down_revision = '68ad0dadaafd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
