"""in users table email & password column is altered to not null

Revision ID: 88236ed6425d
Revises: 7f705f41d713
Create Date: 2026-06-12 16:18:26.350139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88236ed6425d'
down_revision = '7f705f41d713'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users','email',nullable=False)
    op.alter_column('users','password',nullable = False)
                    
    pass


def downgrade():
    op.alter_column('users','email',nullable=True)
    op.alter_column('users','password',nullable=True)
    pass
