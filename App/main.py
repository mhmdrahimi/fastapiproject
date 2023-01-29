from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import schema

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/", tags=["user"])
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


# find Todos with id
@app.get("/user/{user_id}", tags=["user"])
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail="not found")


@app.post("/user/", tags=["user"])
async def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    users = models.Users()
    users.email = user.email
    users.username = user.username
    users.firstname = user.firstname
    users.lastname = user.lastname

    db.add(users)
    db.commit()

    return "success"


@app.put("/user/{user_id}", tags=["user"])
async def update_user(user_id: int, todo: schema.User, db: Session = Depends(get_db)):
    users = db.query(models.Users) \
        .filter(models.Users.id == user_id) \
        .first()

    if users is None:
        raise HTTPException(status_code=404, detail="not found")

    users.email = todo.email
    users.username = todo.username
    users.firstname = todo.firstname
    users.lastname = todo.lastname
    db.add(users)
    db.commit()
    return "success"


@app.delete("/{user_id}", tags=["user"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    users = db.query(models.Users) \
        .filter(models.Users.id == user_id) \
        .first()

    if users is None:
        raise HTTPException(status_code=404, detail="not found")

    db.query(models.Users) \
        .filter(models.Users.id == user_id) \
        .delete()

    db.commit()

    return "success"


@app.get("/todo", tags=["todo"])
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get("/todo/{todo_id}", tags=["todo"])
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail="not found")


@app.post("/todo/", tags=["todo"])
async def create_todo(todo: schema.CreateTodo, db: Session = Depends(get_db)):
    todos = models.Todos()
    todos.title = todo.title
    todos.description = todo.description
    todos.priority = todo.priority
    todos.complete = todo.complete

    db.add(todos)
    db.commit()

    return "success"


@app.put("/todo/{todo_id}", tags=["todo"])
async def update_todo(todo_id: int, todo: schema.Todo, db: Session = Depends(get_db)):
    todos = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .first()

    if todos is None:
        raise HTTPException(status_code=404, detail="not found")

    todos.title = todo.title
    todos.description = todo.description
    todos.priority = todo.priority
    todos.complete = todo.complete

    db.add(todos)
    db.commit()

    return "success"


@app.delete("/{todo_id}", tags=["todo"])
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todos = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .first()

    if todos is None:
        raise HTTPException(status_code=404, detail="not found")

    db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .delete()

    db.commit()

    return "success"
