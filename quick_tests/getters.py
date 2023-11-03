from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api_v1.projects.models import Project
from src.api_v1.tasks.models import Task, TaskComment
from src.api_v1.teams.models import Team
from src.api_v1.users.models import User, UserProfile


class GetEntity:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        user: User | None = await self.session.scalar(stmt)
        if user is None:
            return user
        print(f"Get user by id: id={user.id}, username={user.username}")
        return user

    async def get_user_profile_by_user_id(self, user_id: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.user_id == user_id)
        result: Result = await self.session.execute(stmt)
        user_profile: UserProfile | None = result.scalar_one_or_none()
        print(f"Get user_profile: profile={user_profile}")
        return user_profile

    async def get_project_by_id(self, project_id: UUID) -> Project | None:
        stmt = select(Project).where(Project.id == project_id)
        result: Result = await self.session.execute(stmt)
        project: Project = result.scalar_one_or_none()
        print(f"Get project: id={project.id}, name={project.name}")
        return project

    async def get_task_by_id(self, task_id: UUID) -> Task | None:
        stmt = select(Task).where(Task.id == task_id)
        result: Result = await self.session.execute(stmt)
        task: Task = result.scalar_one_or_none()
        print(f"Get task: id={task.id}, title={task.title}")
        return task

    async def get_task_comment_by_task_id(self, task_id: UUID) -> TaskComment | None:
        stmt = select(TaskComment).where(TaskComment.task_id == task_id)
        result: Result = await self.session.execute(stmt)
        comment: TaskComment = result.scalar_one_or_none()
        print(f"Get task_comment: id={comment.id}, title={comment.title}")
        return comment

    async def get_team_by_id(self, team_id: UUID) -> Team | None:
        stmt = select(Team).where(Team.id == team_id)
        result: Result = await self.session.execute(stmt)
        team: Team = result.scalar_one_or_none()
        print(f"Get team: id={team.id}, title={team.title}")
        return team


class GetEntityWithRelations:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_users_with_profiles(self) -> list[User]:
        stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
        # stmt = select(User).options(selectinload(User.profile)).order_by(User.id)
        users: list[User] = await self.session.scalars(stmt)
        for user in users:
            print(f"Get User: {user.username}")
            print(
                f"User profile first name: {user.profile.first_name if user.profile else None}"  # noqa
            )
        return list(users)

    async def get_users_with_tasks(self) -> list[User]:
        stmt = select(User).options(selectinload(User.tasks)).order_by(User.id)
        result: Result = await self.session.execute(stmt)
        users: list[User] = result.scalars()
        for user in users:  # type: User
            print(f"Get User: {user.username}")
            for ut in user.tasks:
                print("-- ", f"Owner of task: {ut.title}")
        return users

    async def get_users_with_all(self) -> list[User]:
        stmt = (
            select(User)
            .options(
                joinedload(User.profile),
                selectinload(User.projects),
                selectinload(User.tasks),
            )
            .order_by(User.created_at)
        )
        result: Result = await self.session.execute(stmt)
        users: list[User] = result.scalars()
        for user in users:
            print(f"User: {user.username}")
            print(f"User Profile: {user.profile}")
            for p in user.projects:
                print(f"-- In project: {p.name}")  # noqa
            for t in user.tasks:
                print(f"-- In task: {t.title}")
        return users

    async def get_projects_with_all(self) -> list[User]:  # noqa
        stmt = (
            select(Project)
            .options(
                selectinload(Project.users),
                selectinload(Project.tasks),
                # selectinload(Project.teams),
            )
            .order_by(Project.created_at)
        )
        result: Result = await self.session.execute(stmt)
        projects: list[Project] = result.scalars()
        for p in projects:
            print(f"Get Project: {p.name}")
            for u in p.users:
                print(f"-- User in project: {u.username}")  # noqa
            for t in p.tasks:
                print(f"-- Task in project: {t.title}")
        return projects

    async def get_teams_with_all(self) -> list[Team]:
        stmt = select(Team).options(joinedload(Team.users)).order_by(Team.created_at)
        result: Result = await self.session.execute(stmt)
        teams: list[Team] = result.scalars().unique()
        for t in teams:
            print(f"Team: {t.title}")
            for u in t.users:
                print(f"-- User in team: {u.username}")  # noqa
        return teams

    async def get_tasks_with_all(self) -> list[Task]:
        stmt = (
            select(Task)
            .options(
                joinedload(Task.project),
                selectinload(Task.users),
                selectinload(Task.comments),
            )
            .order_by(Task.id)
        )
        result: Result = await self.session.execute(stmt)
        tasks: list[Task] = result.scalars()
        for task in tasks:
            print(f"Get Task: {task.title};")
            for user in task.users:
                print(f"-- User in task: {user.username}")
            for comment in task.comments:
                print(f"-- Comment in task: {comment.content}")
        return tasks
