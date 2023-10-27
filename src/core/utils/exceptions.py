from fastapi import HTTPException, status

users_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User(-s) not found!"
)
