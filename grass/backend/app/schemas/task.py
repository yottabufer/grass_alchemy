from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, description="Title cannot be empty")
    completed: Optional[bool] = Field(False, description="Completed must be a boolean")

    @validator('completed', pre=True)
    def validate_completed(cls, v):
        if isinstance(v, bool):
            return v
        raise ValueError("Completed type error")


class TaskCreate(TaskBase):
    pass


class TaskInDB(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
