"""rename usersprofile to profiles, alter associate tables

Revision ID: 94d0d83db26e
Revises: 083473de6de2
Create Date: 2023-11-08 15:23:04.143159

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "94d0d83db26e"
down_revision: Union[str, None] = "083473de6de2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "profiles",
        sa.Column("first_name", sa.String(length=32), nullable=True),
        sa.Column("last_name", sa.String(length=32), nullable=True),
        sa.Column("avatar_url", sa.String(length=256), nullable=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users_teams",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("team_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "team_id", name="unique_users_teams"),
    )
    op.create_table(
        "users_projects",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "project_id", name="unique_users_projects"),
    )
    op.create_table(
        "users_tasks",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("task_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "task_id", name="unique_users_tasks"),
    )
    op.drop_table("teams_projects")
    op.drop_table("userprofiles")
    op.add_column("projects", sa.Column("team_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        None,
        "projects",
        "teams",
        ["team_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "projects", type_="foreignkey")
    op.drop_column("projects", "team_id")
    op.create_table(
        "userprofiles",
        sa.Column(
            "first_name", sa.VARCHAR(length=32), autoincrement=False, nullable=True
        ),
        sa.Column("last_name", sa.VARCHAR(length=32), autoincrement=False, nullable=True),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "avatar_url", sa.VARCHAR(length=256), autoincrement=False, nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="userprofiles_user_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="userprofiles_pkey"),
    )
    op.create_table(
        "teams_projects",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("team_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("project_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.id"], name="teams_projects_project_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["team_id"], ["teams.id"], name="teams_projects_team_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="teams_projects_pkey"),
        sa.UniqueConstraint("team_id", "project_id", name="unique_team_projects"),
    )
    op.drop_table("users_tasks")
    op.drop_table("users_projects")
    op.drop_table("users_teams")
    op.drop_table("profiles")
    # ### end Alembic commands ###
