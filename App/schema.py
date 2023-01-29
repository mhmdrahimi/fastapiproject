from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    username: str
    email: Optional[str]
    firstname: str
    lastname: str


class CreateUser(User):
    pass


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool


class CreateTodo(Todo):
    pass
