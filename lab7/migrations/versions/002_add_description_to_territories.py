"""Добавление описания к территориям

Revision ID: 002_add_description_to_territories
Revises: 001_create_territories_metrics
Create Date: 2026-06-04

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002_add_description"
down_revision: Union[str, None] = "001_create_territories_metrics"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "territories",
        sa.Column("description", sa.String(length=500), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("territories", "description")
