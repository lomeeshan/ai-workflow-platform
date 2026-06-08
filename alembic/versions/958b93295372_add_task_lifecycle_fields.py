"""add task lifecycle fields

Revision ID: 958b93295372
Revises: 01afdd100124
Create Date: 2026-06-08 11:29:43.162789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '958b93295372'
down_revision: Union[str, Sequence[str], None] = '01afdd100124'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "task",
        sa.Column(
            "status",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
            server_default="pending",
        ),
    )

    op.add_column(
        "task",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    op.add_column(
        "task",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    op.alter_column("task", "status", server_default=None)
    op.alter_column("task", "created_at", server_default=None)
    op.alter_column("task", "updated_at", server_default=None)           

def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("task", "updated_at")
    op.drop_column("task", "created_at")
    op.drop_column("task", "status")



