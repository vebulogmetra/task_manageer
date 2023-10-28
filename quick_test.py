import asyncio
import random
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.core.models.project import Project
from src.core.models.task import Task, TaskComment
from src.core.models.user import User
from src.core.models.user_profile import UserProfile
from src.core.utils.database import db_helper


class CreateEntity:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def create_user(self, username: str) -> User:
        user: User = User(username=username)
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
        self, user_id: str, name: str, description: str
    ) -> Project:
        project: Project = Project(user_id=user_id, name=name, description=description)
        self.session.add(project)
        await self.session.commit()
        print(f"Crated project: {project.name}")
        return project

    async def create_task(
        self,
        user_id: str,
        project_id: str,
        title: str,
        description: str,
        status: str,
        priority: str,
        due_date: datetime,
    ) -> Task:
        task: Task = Task(
            user_id=user_id,
            project_id=project_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
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


class CreateMoreEntity:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def create_more_projects(
        self,
        user_id: str,
    ) -> list[Project]:
        generated_data: list[tuple] = []
        for _ in range(3):
            name = f"Projec Name {uuid4().hex}"
            description = f"Description {uuid4().hex}"
            generated_data.append((name, description))
        projects = [
            Project(user_id=user_id, name=name, description=descr)
            for name, descr in generated_data
        ]
        self.session.add_all(projects)
        await self.session.commit()
        print(f"Created projects: {projects}")
        return projects

    async def create_more_tasks(
        self,
        user_id: str,
        project_id: str,
    ) -> list[Task]:
        due_dates: list[datetime] = []
        for _ in range(5):
            due_dates.append(
                datetime.now().replace(microsecond=0)
                + timedelta(days=random.randint(1, 7))
            )
        tasks = [
            Task(user_id=user_id, project_id=project_id, due_date=dd)
            for dd in due_dates
        ]
        self.session.add_all(tasks)
        await self.session.commit()
        print(f"Created tasks: {tasks}")
        return tasks

    async def create_more_task_comments(
        self,
        user_id: str,
        task_id: str,
    ) -> list[TaskComment]:
        contents: list[str] = []
        for _ in range(5):
            contents.append(f"Comment_{uuid4().hex[:8]}")
        task_comments = [
            TaskComment(user_id=user_id, task_id=task_id, content=co) for co in contents
        ]
        self.session.add_all(task_comments)
        await self.session.commit()
        print(f"Created task_comments: {task_comments}")
        return task_comments


class GetEntityWithRelations:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_users_with_tasks(self) -> list[User]:
        stmt = select(User).options(selectinload(User.tasks)).order_by(User.id)
        result: Result = await self.session.execute(stmt)
        users: list[User] = result.scalars()
        for user in users:
            print(f"User: {user.username}")
            for ut in user.tasks:
                print("- ", f"User task title: {ut.title}")
        return users

    async def get_tasks_with_users(self) -> list[Task]:
        stmt = select(Task).options(joinedload(Task.user)).order_by(Task.id)
        result: Result = await self.session.execute(stmt)
        tasks: list[Task] = result.scalars()
        for task in tasks:
            print(f"Task: {task.title}")
            print(f"Task User: {task.user.username}")
        return tasks

    async def get_users_with_profiles(self) -> list[User]:
        stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
        # stmt = select(User).options(selectinload(User.profile)).order_by(User.id)
        users: list[User] = await self.session.scalars(stmt)
        for user in users:
            print(f"User: {user.username}")
            print(
                f"User profile first name: {user.profile.first_name if user.profile else None}"
            )
        return users

    async def get_users_with_profiles_and_with_tasks(self) -> list[User]:
        stmt = (
            select(User)
            .options(joinedload(User.profile), selectinload(User.tasks))
            .order_by(User.id)
        )
        result: Result = await self.session.execute(stmt)
        users: list[User] = result.scalars()
        for user in users:
            print(f"User: {user.username}")
            print(
                f"User profile first_name: {user.profile.first_name if user.profile else None}"
            )
            for ut in user.tasks:
                print("- ", f"User task title: {ut.title}")
        return users


async def run_without_create():
    async with db_helper.session_factory() as session:
        getter: GetEntity = GetEntity(session)
        getter_with: GetEntityWithRelations = GetEntityWithRelations(session)
        await getter.get_user_by_username(username="string")  # Not exists
        await getter.get_user_by_username(username="ivan")
        await getter.get_user_by_username(username="viktor")
        await getter.get_user_by_username(username="john")
        await getter.get_project_by_name(name="IvanProject")
        await getter.get_task_by_title(title="Task for John")

        _: list[User] = await getter_with.get_users_with_tasks()
        _: list[Task] = await getter_with.get_tasks_with_users()
        _: list[User] = await getter_with.get_users_with_profiles_and_with_tasks()
        _: list[User] = await getter_with.get_users_with_profiles()


async def run_create():
    async with db_helper.session_factory() as session:
        creater: CreateEntity = CreateEntity(session)
        creater_more: CreateMoreEntity = CreateMoreEntity(session)
        user_ivan: User = await creater.create_user(username="ivan")
        user_viktor: User = await creater.create_user(username="viktor")
        user_john: User = await creater.create_user(username="john")
        await creater.create_user_profile(
            user_id=user_ivan.id, first_name="Ivan", last_name="Jobs"
        )
        await creater.create_user_profile(
            user_id=user_john.id, first_name="John", last_name="Doe"
        )
        project: Project = await creater.create_project(
            user_id=user_ivan.id,
            name="IvanProject",
            description="lalala some description string lalala",
        )
        _: Task = await creater.create_task(
            user_id=user_john.id,
            project_id=project.id,
            title="Task for John",
            description="Add product model in db, and create API",
            status="created",  # created, in_work, complete
            priority="high",  # low, medium, high
            due_date=datetime.now() + timedelta(weeks=2),
        )

        _: list[Task] = await creater_more.create_more_tasks(
            session,
            user_john.id,
            project.id,
        )

        projects_ivan: list[Project] = await creater_more.create_more_projects(
            session, user_ivan.id
        )
        projects_viktor: list[Project] = await creater_more.create_more_projects(
            session, user_viktor.id
        )
        for pi in projects_ivan:
            user_id = random.choice([user_ivan.id, user_viktor.id, user_john.id])
            _: list[Task] = await creater_more.create_more_tasks(
                session,
                user_id,
                pi.id,
            )
        for pv in projects_viktor:
            user_id = random.choice([user_ivan.id, user_viktor.id, user_john.id])
            _: list[Task] = await creater_more.create_more_tasks(
                session,
                user_id,
                pv.id,
            )


if __name__ == "__main__":
    # asyncio.run(run_create())
    asyncio.run(run_without_create())
