from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models.token import Token
from ..models.user import User
from ..services.user_service import register, login

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", summary="Register a new user")
async def post_signup(user: User) -> Token:
    return register(user=user)


@router.post("/token", summary="Request an access token")
async def post_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    return login(form_data=form_data)
