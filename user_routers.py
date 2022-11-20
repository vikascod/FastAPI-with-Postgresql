from fastapi import APIRouter, Depends, HTTPException, status
from models import User
import schemas
from database import get_db
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from JWTtoken import create_access_token

user_router = APIRouter(
    tags=['Users']
)

@user_router.post('/signup', status_code=status.HTTP_201_CREATED)
def signup(user:schemas.UserSchema, db:Session=Depends(get_db)):
    new_user = User(username=user.username, email=user.email, password=generate_password_hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@user_router.get('/user/{id}', response_model=schemas.UserModel, status_code=status.HTTP_200_OK)
def show(id, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user available with id {id}")
    return user



@user_router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    # if not check_password_hash(user.password, request.password):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}