from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from Database.user_operations import (
    insert_user,
    user_exists,
    get_user_data,
    update_points,
    UserModel,
    get_scores,
    ScoreModel,
)

from ..models.token import Token
from ..models.user import User

from ...util.security import (
    hash_password,
    verify_password,
    create_access_token,
)


# -----------------------------
# User retrieval & authentication
# -----------------------------

def get_user(username: str) -> UserModel:
    """
    Retrieve a user from the database.
    """
    return get_user_data(username=username)


def authenticate_user(username: str, password: str) -> UserModel | None:
    """
    Authenticate a user by username and password.
    """
    user = get_user(username=username)

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


# -----------------------------
# Auth endpoints logic
# -----------------------------

def register(user: User) -> Token:
    """
    Register a new user and return an access token.
    """
    if user_exists(username=user.username):
        raise HTTPException(status_code=409, detail="Username already exists")

    hashed_password = hash_password(user.password)

    insert_user(
        username=user.username,
        password=hashed_password,
        role="user",
    )

    access_token = create_access_token({"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")


def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Authenticate user and return JWT token.
    """
    user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")
