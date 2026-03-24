from pydantic import BaseModel


class User(BaseModel):
    """
    Userdata for authentication
    """
    username: str
    password: str
