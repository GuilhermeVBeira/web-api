"""Add clients table

Revision ID: 91ef1a91fbc8
Revises: 1595f4d4b09a
Create Date: 2020-10-09 21:56:54.716575

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '91ef1a91fbc8'
down_revision = '1595f4d4b09a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients_client',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clients_client_email'), 'clients_client', ['email'], unique=True)
    op.create_index(op.f('ix_clients_client_username'), 'clients_client', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_clients_client_username'), table_name='clients_client')
    op.drop_index(op.f('ix_clients_client_email'), table_name='clients_client')
    op.drop_table('clients_client')
    # ### end Alembic commands ###
