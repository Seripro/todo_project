from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title:str
    is_completed:bool
    
class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id:int
    created_at:datetime
    updated_at:datetime
    class Config:
        orm_mode = True
        
