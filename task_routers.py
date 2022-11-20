from fastapi import APIRouter, HTTPException, status, Depends
from models import Task
from database import Base, SessionLocal, engine, get_db
import schemas
from sqlalchemy.orm import Session
from oauth2 import get_current_user



task_router = APIRouter(
    prefix='/task',
    tags=['Tasks']
)

@task_router.post('/', status_code=status.HTTP_201_CREATED)
def create(task:schemas.TaskSchema, db:Session=Depends(get_db), current_user:schemas.TaskModel=Depends(get_current_user)):
    new_task = Task(title=task.title, body=task.body, user_id=1)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@task_router.get('/')
def all(db:Session=Depends(get_db), current_user:schemas.TaskModel=Depends(get_current_user)):
    tasks = db.query(Task).all()
    return tasks


@task_router.get('/{id}', response_model=schemas.TaskModel)
def show(id, db:Session=Depends(get_db), current_user:schemas.TaskModel=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task available with id {id}")
    return task


@task_router.delete('/{id}')
def destroy(id, db:Session=Depends(get_db), current_user:schemas.TaskModel=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task available with id {id}")
    db.delete(task)
    db.commit()
    return "Deleted"


@task_router.put('/{id}')
def update(id, request:schemas.TaskSchema, db:Session=Depends(get_db), current_user:schemas.TaskModel=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task available with id {id}")
    task.title = request.title
    task.body = request.body
    db.commit()
    return task