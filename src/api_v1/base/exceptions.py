from fastapi import HTTPException, status


class CustomHTTPException:
    @staticmethod
    def generate_exception(entity_name: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name}(-s) not found!",
        )


custom_exc: CustomHTTPException = CustomHTTPException()
