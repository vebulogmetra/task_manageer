import sqlalchemy as sa

from src.core.models.base import Base

users_tasks = sa.Table(
    "users_tasks",
    Base.metadata,
    sa.Column(
        "id",
        sa.Uuid(),
        server_default=sa.text("gen_random_uuid()"),
        nullable=False,
        primary_key=True,
    ),
    sa.Column("user_id", sa.ForeignKey("users.id")),
    sa.Column("task_id", sa.ForeignKey("tasks.id")),
    sa.UniqueConstraint("user_id", "task_id", name="unique_users_tasks"),
)
