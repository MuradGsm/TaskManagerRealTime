from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    done = "done"


class TaskRequest(BaseModel):
    title: str
    description: str
    status: TaskStatus
    created_by: int
    assigned_to: Optional[int] = None
    watchers: List[int]
    comments: List[str]
    due_date: datetime


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    created_by: int
    assigned_to: Optional[int] = None
    watchers: List[int]
    comments: List[str]
    due_date: datetime
    created_at: datetime

    class Config:
        orm_mode = True
