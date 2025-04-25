import sqlalchemy as sa
from sqlalchemy import MetaData, func
from sqlalchemy.dialects.postgresql import UUID

meta = MetaData()


subscribers = sa.Table(
    "subscribers",
    meta,
    sa.Column("id", UUID, primary_key=True, server_default=func.gen_random_uuid()),
    sa.Column("user_id", UUID, nullable=False),
    sa.Column("email", sa.String(), nullable=False),
    sa.Column("event", sa.String(), nullable=False),
    sa.Column("active", sa.Boolean(), default=True),
    sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.func.current_timestamp(),
        nullable=False,
    ),
    sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.func.current_timestamp(),
        nullable=False,
    ),
)
