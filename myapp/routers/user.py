from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import User
from utils import hash_password
import schemas
from typing import List

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = User(**user.dict())   # unpacked schema pydantic model to our db models
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # display new_user
    return new_user


@router.get("/all", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users_query = db.query(User)
    users = users_query.all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user does not exist")
    return users


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} does not exist")
    return user



