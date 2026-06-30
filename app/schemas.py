from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    """Schema para crear una tarea (lo que recibe la API)."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Priority = Priority.medium


class TaskUpdate(BaseModel):
    """Schema para actualizar una tarea (todos los campos son opcionales)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[Priority] = None


class TaskResponse(BaseModel):
    """Schema de respuesta (lo que devuelve la API)."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
