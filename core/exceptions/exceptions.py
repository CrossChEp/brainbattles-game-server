from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

credentials_exception = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


NO_SUCH_GAME_EXCEPTION = HTTPException(
    status_code=403,
    detail="No game with such token"
)
