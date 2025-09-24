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

def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate):
    # 1. 既存タスクの取得
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    # 2. タスクが存在しない場合はNoneを返す
    if not db_task:
        return None
        
    # 3. 受け取ったデータでタスクを更新
    # model_dump(exclude_unset=True)は、クライアントが指定しなかったフィールドを無視する
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        # setattr(db_task, 'title', '新しいタイトル')はdb_task.title = '新しいタイトル'と同じ意味
        setattr(db_task, key, value)
        
    # 4. データベースへのコミットとリフレッシュ
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task

def delete_task(db: Session, task_id: int):
    # まずタスクを探す
    deleted_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    # もし見つかったら削除
    if deleted_task:
        db.delete(deleted_task)
        db.commit()
    # タスクが見つかったかどうかを返す
    return deleted_task