from sqlalchemy.orm import Session
from . import models, schemas

def get_todo_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.TodoItem).offset(skip).limit(limit).all()

def get_todo_item(db: Session, todo_id: int):
    return db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()

def create_todo_item(db: Session, todo: schemas.TodoItemCreate):
    db_todo = models.TodoItem(title=todo.title, description=todo.description, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo_item(db: Session, todo_id: int, todo: schemas.TodoItemCreate):
    db_todo = db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()
    if db_todo:
        db_todo.title = todo.title
        db_todo.description = todo.description
        db_todo.completed = todo.completed
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo_item(db: Session, todo_id: int):
    db_todo = db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
