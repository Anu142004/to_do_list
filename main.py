from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/todos/", response_model=schemas.TodoItem)
def create_todo_item(todo: schemas.TodoItemCreate, db: Session = Depends(get_db)):
    return crud.create_todo_item(db=db, todo=todo)

@app.get("/todos/", response_model=list[schemas.TodoItem])
def read_todo_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_todo_items(db, skip=skip, limit=limit)

@app.get("/todos/{todo_id}", response_model=schemas.TodoItem)
def read_todo_item(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo_item(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return db_todo

@app.put("/todos/{todo_id}", response_model=schemas.TodoItem)
def update_todo_item(todo_id: int, todo: schemas.TodoItemCreate, db: Session = Depends(get_db)):
    return crud.update_todo_item(db=db, todo_id=todo_id, todo=todo)

@app.delete("/todos/{todo_id}", response_model=schemas.TodoItem)
def delete_todo_item(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo_item(db=db, todo_id=todo_id)
