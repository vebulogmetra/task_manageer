import asyncio
import secrets
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api_v1.projects.models import Project
from src.api_v1.tasks.models import Task
from src.api_v1.users.models import User, UserProfile
from src.core.config import settings
from src.utils.auth import pwd_helper
from src.utils.database import db_manager


class CreateEntity:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def create_user(self, username: str, email: str, password: str) -> User:
        hashed_password = pwd_helper.get_password_hash(password=password)
        user: User = User(username=username, email=email, hashed_password=hashed_password)
        self.session.add(user)
        await self.session.commit()
        print(f"Created user: {user.username}")
        return user

    async def create_user_profile(
        self, user_id: str, first_name: str, last_name: str
    ) -> UserProfile:
        user_profile: UserProfile = UserProfile(
            user_id=user_id, first_name=first_name, last_name=last_name
        )
        self.session.add(user_profile)
        await self.session.commit()
        print(f"Created user_profile: {user_profile.id}")
        return user_profile

    async def create_project(
        self, name: str, description: str, creator_id: str
    ) -> Project:
        project: Project = Project(
            name=name, description=description, creator_id=creator_id
        )
        self.session.add(project)
        await self.session.commit()
        print(f"Crated project: {project.name}")
        return project

    async def add_users_to_project(self, project_id: str, users: list):
        project = await self.session.scalar(
            select(Project)
            .where(Project.id == project_id)
            .options(
                selectinload(Project.users),
            ),
        )

        project.users.extend(users)
        await self.session.commit()

    async def add_users_to_task(self, task_id: str, users: list):
        task = await self.session.scalar(
            select(Task)
            .where(Task.id == task_id)
            .options(
                selectinload(Task.users),
            ),
        )

        task.users.extend(users)
        await self.session.commit()

    async def create_task(
        self,
        project_id: str,
        title: str,
        description: str,
        status: str,
        priority: str,
        due_date: datetime,
        creator_id: str,
    ) -> Task:
        task: Task = Task(
            project_id=project_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            creator_id=creator_id,
        )
        self.session.add(task)
        await self.session.commit()
        print(f"Created task: {task.title}")
        return task


class GetEntity:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        user: User | None = await self.session.scalar(stmt)
        if user is None:
            return user
        print(f"Get user by username: id={user.id}, username={user.username}")
        return user

    async def get_user_profile_by_user_id(self, user_id: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.user_id == user_id)
        result: Result = await self.session.execute(stmt)
        user_profile: UserProfile | None = result.scalar_one_or_none()
        print(f"Get user_profile by user_id: profile={user_profile}")
        return user_profile

    async def get_project_by_name(self, name: str) -> Project | None:
        stmt = select(Project).where(Project.name == name)
        result: Result = await self.session.execute(stmt)
        project: Project = result.scalar_one_or_none()
        print(f"Get project by name: id={project.id}, name={project.name}")
        return project

    async def get_task_by_title(self, title: str) -> Project | None:
        stmt = select(Task).where(Task.title == title)
        result: Result = await self.session.execute(stmt)
        task: Task = result.scalar_one_or_none()
        print(f"Get task by title: id={task.id}, title={task.title}")
        return task


class GetEntityWithRelations:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_users_with_tasks(self) -> list[User]:
        stmt = select(User).options(selectinload(User.tasks)).order_by(User.id)
        result: Result = await self.session.execute(stmt)
        users: list[User] = result.scalars()
        for user in users:  # type: User
            print(f"User: {user.username}")
            for ut in user.tasks:
                print("-- ", f"Owner of task: {ut.title}")
        return users

    async def get_tasks_with_users(self) -> list[Task]:
        stmt = select(Task).options(selectinload(Task.users)).order_by(Task.id)
        result: Result = await self.session.execute(stmt)
        tasks: list[Task] = result.scalars()
        for task in tasks:
            print(f"Task: {task.title}; Task Users:")
            for user in task.users:
                print(f"-- User: {user.username}")
        return tasks

    async def get_projects_with_users(self) -> list[Project]:
        stmt = select(Project).options(selectinload(Project.users)).order_by(Project.id)
        result: Result = await self.session.execute(stmt)
        projects: list[Project] = result.scalars()
        for p in projects:
            print(f"Project: {p.name}; Project Users:")
            for user in p.users:
                print(f"-- User: {user.username}")
        return projects

    async def get_users_with_profiles(self) -> list[User]:
        stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
        # stmt = select(User).options(selectinload(User.profile)).order_by(User.id)
        users: list[User] = await self.session.scalars(stmt)
        for user in users:
            print(f"User: {user.username}")
            print(
                f"User profile first name: {user.profile.first_name if user.profile else None}"  # noqa
            )
        return users

    async def get_users_with_projects_and_with_tasks(self) -> list[User]:
        stmt = (
            select(User)
            .options(selectinload(User.projects), selectinload(User.tasks))
            .order_by(User.id)
        )
        result: Result = await self.session.execute(stmt)
        users: list[User] = result.scalars()
        for user in users:
            print(f"User: {user.username}")
            for p in user.projects:
                print(f"-- In project: {p.name}")  # noqa
            for t in user.tasks:
                print("-- ", f"In task: {t.title}")
        return users


async def run_without_create():
    db_manager.init(connection_url=settings.db_alchemy_url, echo=settings.debug_database)
    async with db_manager.scoped_session_dependency() as session:
        getter: GetEntity = GetEntity(session)
        getter_with: GetEntityWithRelations = GetEntityWithRelations(session)
        await getter.get_user_by_username(username="string")  # Not exists
        await getter.get_user_by_username(username="ivan")
        await getter.get_user_by_username(username="viktor")
        await getter.get_user_by_username(username="john")
        await getter.get_project_by_name(name="IvanProject")
        await getter.get_task_by_title(title="Task for John")

        _: list[User] = await getter_with.get_users_with_profiles()
        _: list[User] = await getter_with.get_users_with_tasks()
        print("#" * 30)
        _: list[Task] = await getter_with.get_tasks_with_users()
        print("#" * 30)
        print("@" * 30)
        _: list[Project] = await getter_with.get_projects_with_users()
        print("@" * 30)
        print("!" * 30)
        _: list[User] = await getter_with.get_users_with_projects_and_with_tasks()
        print("!" * 30)


async def run_create():
    db_manager.init(connection_url=settings.db_alchemy_url, echo=settings.debug_database)
    async with db_manager.scoped_session_dependency() as session:
        creater: CreateEntity = CreateEntity(session)
        user_ivan: User = await creater.create_user(
            username="ivan", email="ivan@gmail.com", password="123"
        )
        user_viktor: User = await creater.create_user(
            username="viktor", email="viktor@gmail.com", password="123"
        )
        user_john: User = await creater.create_user(
            username="john", email="john@gmail.com", password="123"
        )
        _: User = await creater.create_user(
            username="vasya", email="vasya@gmail.com", password="321"
        )
        await creater.create_user_profile(
            user_id=user_ivan.id, first_name="Ivan", last_name="Jobs"
        )
        await creater.create_user_profile(
            user_id=user_john.id, first_name="John", last_name="Doe"
        )
        project_ivan: Project = await creater.create_project(
            name="IvanProject",
            description="lalala some description string lalala",
            creator_id=user_ivan.id,
        )
        project_viktor: Project = await creater.create_project(
            name=f"ViktorProject {secrets.token_urlsafe(16)}",
            description="tatata string tatata",
            creator_id=user_viktor.id,
        )

        await creater.add_users_to_project(
            project_id=project_ivan.id, users=[user_john, user_viktor]
        )
        await creater.add_users_to_project(
            project_id=project_viktor.id, users=[user_john, user_ivan]
        )

        task_ivan: Task = await creater.create_task(
            creator_id=user_ivan.id,
            project_id=project_ivan.id,
            title="Task for John",
            description=f"Add {secrets.token_urlsafe(16)}",
            status="created",  # created, in_work, complete
            priority="high",  # low, medium, high
            due_date=datetime.now() + timedelta(days=secrets.randbelow(20)),
        )
        task_john: Task = await creater.create_task(
            creator_id=user_john.id,
            project_id=project_viktor.id,
            title=f"Task {secrets.token_urlsafe(16)}",
            description=f"{secrets.token_urlsafe(16)} API",
            status="created",  # created, in_work, complete
            priority="high",  # low, medium, high
            due_date=datetime.now() + timedelta(days=secrets.randbelow(20)),
        )

        await creater.add_users_to_task(
            task_id=task_ivan.id, users=[user_viktor, user_john]
        )
        await creater.add_users_to_task(
            task_id=task_john.id, users=[user_john, user_ivan]
        )


if __name__ == "__main__":
    # asyncio.run(run_create())
    asyncio.run(run_without_create())
