"""Add favorite products table

Revision ID: e7642fcb8c04
Revises: 91ef1a91fbc8
Create Date: 2020-10-10 15:29:57.763153

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e7642fcb8c04"
down_revision = "91ef1a91fbc8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "clients_favorite_product",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("client_id", postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["clients_client.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("clients_favorite_product")
    # ### end Alembic commands ###
