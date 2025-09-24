from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title:str
    is_completed:bool = False
    
    
# クライアントからのリクエストの型
class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = False


# APIからのレスポンスの型
class Task(TaskBase):
    id:int
    created_at:datetime
    updated_at:datetime
    class Config:
        orm_mode = True
        
class TaskDelete(BaseModel):
    message: str
        
