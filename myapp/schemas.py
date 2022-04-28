from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint


# Pydantic model to define schema for post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True      # optional field | if doesnt provide published, default = True


class CreatePost(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut

    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict,
    # but an ORM model (or any other arbitrary object with attributes).By default pydantic model read only dict
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int


class UpdatePost(PostBase):
    title: str
    content: str


class CreateUser(BaseModel):
    email: EmailStr
    password: str


# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
