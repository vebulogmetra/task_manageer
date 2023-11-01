import sqlalchemy as sa

from src.core.models.base import Base

users_projects = sa.Table(
    "users_projects",
    Base.metadata,
    sa.Column(
        "id",
        sa.Uuid(),
        server_default=sa.text("gen_random_uuid()"),
        nullable=False,
        primary_key=True,
    ),
    sa.Column("user_id", sa.ForeignKey("users.id")),
    sa.Column("project_id", sa.ForeignKey("projects.id")),
    sa.UniqueConstraint("user_id", "project_id", name="unique_users_projects"),
)
