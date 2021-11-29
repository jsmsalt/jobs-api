"""'Initial_Data'

Revision ID: 30e600522ff4
Revises: b289bd3d7995
Create Date: 2021-11-26 13:35:53.902882

"""
from migrations.initial_data import tables
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30e600522ff4'
down_revision = 'b289bd3d7995'
branch_labels = None
depends_on = None


def upgrade():
    meta = sa.MetaData(bind=op.get_bind())
    for table_name, rows in tables.items():
        table = sa.Table(table_name, meta, autoload=True)
        op.bulk_insert(table, rows)


def downgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.drop_all(bind=op.get_bind())
