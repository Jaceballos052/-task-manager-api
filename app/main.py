from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db
from . import models, schemas, crud

# Crea las tablas en la BD si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="API REST para gestión de tareas — construida con FastAPI, PostgreSQL y Docker",
    version="1.0.0",
    contact={
        "name": "José Ángel Ceballos",
        "url": "https://github.com/Jaceballos052",
    },
)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "message": "Task Manager API is running"}


@app.get("/tasks", response_model=List[schemas.TaskResponse], tags=["tasks"])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Devuelve todas las tareas con paginación opcional."""
    return crud.get_tasks(db, skip=skip, limit=limit)


@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Crea una nueva tarea."""
    return crud.create_task(db, task)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Obtiene una tarea por su ID."""
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["tasks"])
def update_task(task_id: int, task_data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Actualiza parcialmente una tarea (solo los campos enviados)."""
    task = crud.update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Elimina una tarea por su ID."""
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
