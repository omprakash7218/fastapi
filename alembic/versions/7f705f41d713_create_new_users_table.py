"""create new users table

Revision ID: 7f705f41d713
Revises: 47b1e3df3f61
Create Date: 2026-06-12 15:56:44.518480

"""
from psycopg2 import Timestamp

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f705f41d713'
down_revision = '47b1e3df3f61'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=True),
                    sa.Column('password',sa.String(),nullable=True),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
