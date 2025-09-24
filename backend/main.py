from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    # フロントのURL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# タスクを全件取得
@app.get("/tasks/", response_model=list[schemas.Task])
def get_tasks(db:Session=Depends(get_db)):
    tasks=crud.get_tasks(db)
    return tasks

@app.get("/task/{task_id}",response_model=schemas.Task)
def get_task(task_id:int,db:Session=Depends(get_db)):
    db_task=crud.get_task(task_id=task_id, db=db)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# タスクを新規登録
@app.post("/tasks/", response_model=schemas.Task)
def create_task(task:schemas.TaskCreate, db:Session=Depends(get_db)):
    return crud.create_task(db=db, task=task)

# タスクを更新(タイトル、完了状態)
@app.put("/tasks/{task_id}",response_model=schemas.Task)
def update_task_endpoint(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    # crud関数を呼び出してタスクを更新
    updated_task = crud.update_task(db=db, task_id=task_id, task_data=task)
    
    # タスクが見つからない場合はHTTP 404エラーを返す
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # 更新されたタスクをJSONとして返す
    return updated_task

# タスクの削除
@app.delete("/tasks/{task_id}",response_model=schemas.TaskDelete)
def delete_task(task_id:int, db:Session=Depends(get_db)):
    deleted_task=crud.delete_task(task_id=task_id, db=db)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message":"Task deleted successfully"}