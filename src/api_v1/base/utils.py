from typing import Optional
from uuid import UUID


def is_valid_uuid(value: str, version: Optional[int] = 4) -> bool:
    """
    Check if value is a valid UUID.

     Parameters
    ----------
    value : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if value is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    if isinstance(value, UUID):
        return True
    try:
        uuid_obj = UUID(value, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == value
