from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


### User
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado")

    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# User info
@app.get("/users/{user_id}", response_model=schemas.User)
def find_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)


# Edit User
@app.put("/users/{user_id}", response_model=schemas.User)
async def edit_user(user_id: int, new_value: schemas.UserEdit, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user:
        return crud.edit_user(db, user_id, new_value=new_value)
    
    raise HTTPException(status_code=400, detail="Usuário não encontrado")


@app.patch("/users/{user_id}", response_model=schemas.User)
async def edit_user(user_id: int, new_value: schemas.UserEdit, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user:
        return crud.edit_user(db, user_id, new_value=new_value)
    
    raise HTTPException(status_code=400, detail="Usuário não encontrado")


# Measure
@app.get("/measures/", response_model=List[schemas.Measure])
def read_measures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_measures(db, skip=skip, limit=limit)
    return users


@app.post("/users/{user_id}/measures/", response_model=schemas.Measure)
def create_measure(user_id: int, measure: schemas.MeasureCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user:
        return crud.create_user_measure(db, measure, user_id)

    raise HTTPException(status_code=400, detail="Usuário não encontrado")


@app.get("/users/{user_id}/measures/", response_model=List[schemas.Measure])
def get_user_measure(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user:
        return crud.get_user_measure(db, user_id)

    raise HTTPException(status_code=400, detail="Usuário não encontrado")