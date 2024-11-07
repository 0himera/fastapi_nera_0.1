"""обавление изображений в продукт

Revision ID: c7ce5b43afd3
Revises: 5dcb8937ebec
Create Date: 2024-11-04 20:58:22.133919

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c7ce5b43afd3"
down_revision: Union[str, None] = "5dcb8937ebec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
    )
    op.create_table(
        "images",
        sa.Column("url", sa.String(length=255), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_images_product_id_products"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_images")),
    )


def downgrade() -> None:
    op.drop_table("images")
    op.drop_table("products")
