"""create appointments table"""
from alembic import op
import sqlalchemy as sa

revision = "0001_create_appointments"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("student_name", sa.String(length=120), nullable=False),
        sa.Column("tutor", sa.String(length=120), nullable=False),
        sa.Column("subject", sa.String(length=120), nullable=False),
        sa.Column("class_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="BOOKED"),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_table("appointments")
