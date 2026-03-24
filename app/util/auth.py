from typing import Annotated
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from Config.jwt_config import SECRET_KEY, ALGORITHM
from Database.user_operations import UserModel
from Microservice.user_service import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_user_token(token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if username is None:
            raise credentials_exception

    except InvalidTokenError as e:
        raise credentials_exception from e

    user = get_user(username=username)

    if user is None:
        raise credentials_exception

    return user
