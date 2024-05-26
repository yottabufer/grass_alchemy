from fastapi import HTTPException
from pydantic import BaseModel, Field, validator, field_validator
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, description='Title cannot be empty')
    completed: Optional[bool] = Field(False, description='Completed must be a boolean')

    @field_validator('completed', mode='before')
    def validate_completed(cls, value):
        if isinstance(value, bool):
            return value
        raise HTTPException(status_code=400, detail='Completed must be a boolean')

    @field_validator('title', mode='before')
    def validate_title(cls, value):
        if isinstance(value, str):
            return value
        raise HTTPException(status_code=400, detail='The title cannot be empty')


class TaskCreate(TaskBase):
    pass


class TaskInDB(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True
