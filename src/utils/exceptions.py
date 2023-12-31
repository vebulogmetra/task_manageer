from fastapi import HTTPException, status


class EmptyAuthCookie(Exception):
    ...


class CustomHTTPException:
    @staticmethod
    def not_found(entity_name: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name}(-s) not found!",
        )

    @staticmethod
    def unauthorized(detail: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{detail}",
        )

    @staticmethod
    def internal_error(detail: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{detail}",
        )

    @staticmethod
    def invalid_input(detail: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{detail}",
        )

    @staticmethod
    def empty_auth_cookie():
        return EmptyAuthCookie("Emty auth cookie")


custom_exc: CustomHTTPException = CustomHTTPException()
