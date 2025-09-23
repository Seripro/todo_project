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
        
@app.get("/tasks/", response_model=list[schemas.Task])
def get_tasks(db:Session=Depends(get_db)):
    tasks=crud.get_tasks(db)
    return tasks

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task:schemas.TaskCreate, db:Session=Depends(get_db)):
    return crud.create_task(db=db, task=task)