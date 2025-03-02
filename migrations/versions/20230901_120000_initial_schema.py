"""Initial schema

Revision ID: 71f05d23bd70
Revises: 
Create Date: 2023-09-01 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

revision = "71f05d23bd70"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "premium_calculations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("car_make", sa.String(), nullable=False),
        sa.Column("car_model", sa.String(), nullable=False),
        sa.Column("car_year", sa.Integer(), nullable=False),
        sa.Column("car_value", sa.Float(), nullable=False),
        sa.Column("deductible_percentage", sa.Float(), nullable=False),
        sa.Column("broker_fee", sa.Float(), nullable=False),
        sa.Column("has_location", sa.Boolean(), nullable=False, default=False),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("postal_code", sa.String(), nullable=True),
        sa.Column("applied_rate", sa.Float(), nullable=False),
        sa.Column("base_premium", sa.Float(), nullable=False),
        sa.Column("deductible_value", sa.Float(), nullable=False),
        sa.Column("policy_limit", sa.Float(), nullable=False),
        sa.Column("calculated_premium", sa.Float(), nullable=False),
        sa.Column("request_data", JSON(), nullable=False),
        sa.Column("response_data", JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_premium_calculations_car_make"),
        "premium_calculations",
        ["car_make"],
        unique=False,
    )
    op.create_index(
        op.f("ix_premium_calculations_car_model"),
        "premium_calculations",
        ["car_model"],
        unique=False,
    )
    op.create_index(
        op.f("ix_premium_calculations_created_at"),
        "premium_calculations",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_premium_calculations_state"),
        "premium_calculations",
        ["state"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        op.f("ix_premium_calculations_state"), table_name="premium_calculations"
    )
    op.drop_index(
        op.f("ix_premium_calculations_created_at"), table_name="premium_calculations"
    )
    op.drop_index(
        op.f("ix_premium_calculations_car_model"), table_name="premium_calculations"
    )
    op.drop_index(
        op.f("ix_premium_calculations_car_make"), table_name="premium_calculations"
    )

    op.drop_table("premium_calculations")
