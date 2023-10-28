from fastapi import HTTPException, status

users_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User(-s) not found!"
)

tasks_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Task(-s) not found!"
)

projects_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Project(-s) not found!"
)
