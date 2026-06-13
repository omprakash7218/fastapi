"""add posts table to the database

Revision ID: 68ad0dadaafd
Revises: 
Create Date: 2026-06-12 15:16:49.432994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68ad0dadaafd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String(),nullable=False)
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
