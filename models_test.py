
from pydantic import BaseModel
from typing import Union
class Token(BaseModel):
    access_token: str
    token_type: str
    is_super_user: bool


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    super_user: bool
    company: str
    entities: list


class Entities(BaseModel):
    entity_list: list


class UserInDB(User):
    hashed_password: str