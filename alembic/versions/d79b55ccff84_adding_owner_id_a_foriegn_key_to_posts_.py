"""adding owner id a foriegn key to posts table'

Revision ID: d79b55ccff84
Revises: 514a25eb78f5
Create Date: 2026-06-12 17:00:30.682061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd79b55ccff84'
down_revision = '514a25eb78f5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')

    pass


def downgrade():
    op.drop_constraint('post_user_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass