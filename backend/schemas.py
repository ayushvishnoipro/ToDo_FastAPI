from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

# User schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    status: StatusEnum = StatusEnum.pending

class Task(TaskBase):
    id: int
    status: StatusEnum
    owner_id: int

    class Config:
        orm_mode = True
        
    # Convert Enum to string when returning as JSON
    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        if isinstance(data.get("status"), StatusEnum):
            data["status"] = data["status"].value
        return data