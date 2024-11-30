"""Add feedbacks

Revision ID: 316f232863d8
Revises: c7ce5b43afd3
Create Date: 2024-11-29 23:16:50.795945

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "316f232863d8"
down_revision: Union[str, None] = "c7ce5b43afd3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "feedbacks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_feedbacks_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_feedbacks")),
    )


def downgrade() -> None:
    op.drop_table("feedbacks")
