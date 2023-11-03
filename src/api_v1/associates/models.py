import sqlalchemy as sa

from src.api_v1.base.models import Base

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

teams_projects = sa.Table(
    "teams_projects",
    Base.metadata,
    sa.Column(
        "id",
        sa.Uuid(),
        server_default=sa.text("gen_random_uuid()"),
        nullable=False,
        primary_key=True,
    ),
    sa.Column("team_id", sa.ForeignKey("teams.id")),
    sa.Column("project_id", sa.ForeignKey("projects.id")),
    sa.UniqueConstraint("team_id", "project_id", name="unique_team_projects"),
)

users_teams = sa.Table(
    "users_teams",
    Base.metadata,
    sa.Column(
        "id",
        sa.Uuid(),
        server_default=sa.text("gen_random_uuid()"),
        nullable=False,
        primary_key=True,
    ),
    sa.Column("user_id", sa.ForeignKey("users.id")),
    sa.Column("team_id", sa.ForeignKey("teams.id")),
    sa.UniqueConstraint("user_id", "team_id", name="unique_users_teams"),
)
