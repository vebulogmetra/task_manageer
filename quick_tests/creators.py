from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api_v1.projects.models import Project
from src.api_v1.tasks.models import Task, TaskComment
from src.api_v1.teams.models import Team
from src.api_v1.users.models import User, UserProfile
from src.utils.auth import pwd_helper


class Creator:
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

    async def create_task_comment(self, user_id: str, task_id: str, content: str):
        comment = TaskComment(content=content, user_id=user_id, task_id=task_id)
        self.session.add(comment)
        await self.session.commit()
        print(f"Created task_comment: {comment.content}")
        return comment

    async def create_team(self, creator_id: str, title: str):
        team = Team(title=title, creator_id=creator_id)
        self.session.add(team)
        await self.session.commit()
        print(f"Created team: {team.title}")
        return team


class AddToEntity:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def add_users_to_project(self, project_id: str, users: list):
        project: Project = await self.session.scalar(
            select(Project)
            .where(Project.id == project_id)
            .options(
                selectinload(Project.users),
            ),
        )

        project.users.extend(users)
        await self.session.commit()

    async def add_users_to_task(self, task_id: str, users: list):
        task: Task = await self.session.scalar(
            select(Task)
            .where(Task.id == task_id)
            .options(
                selectinload(Task.users),
            ),
        )

        task.users.extend(users)
        await self.session.commit()

    async def add_users_to_team(self, team_id: str, users: list):
        team: Team = await self.session.scalar(
            select(Team)
            .where(Team.id == team_id)
            .options(
                selectinload(Team.users),
            ),
        )

        team.users.extend(users)
        await self.session.commit()

    # async def add_team_to_project(self, project_id: str, teams: list):
    #     project: Project = await self.session.scalar(
    #         select(Project)
    #         .where(Project.id == project_id)
    #         .options(
    #             selectinload(Project.users),
    #         ),
    #     )

    #     project.users.extend(teams)
    #     await self.session.commit()
