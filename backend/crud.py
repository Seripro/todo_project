from sqlalchemy.orm import Session
from . import models, schemas

def get_tasks(db:Session):
    return db.query(models.Task).all()

def get_task(db:Session, task_id:int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def create_task(db:Session, task:schemas.TaskCreate):
    db_task = models.Task(title=task.title)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    print(db_task)
    return db_task

def update_task(db:Session, task_id:int, new_title:str):
    updated_task=db.query(models.Task).filter(models.Task.id == task_id).first()
    updated_task.title = new_title
    db.commit()
    return updated_task

def delete_task(db:Session, task_id:int):
    deleted_task=db.query(models.Task).filter(models.Task.id == task_id).first()
    db.delete(deleted_task)
    db.commit()
    return {"message":"Task deleted successfully"}