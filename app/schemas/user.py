from pydantic import BaseModel, EmailStr
from typing import Literal


class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["candidate", "employer"]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str