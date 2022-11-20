from pydantic import BaseModel
from typing import List


class TaskSchema(BaseModel):
    title : str
    body : str

class TaskModel(BaseModel):
    title : str
    body : str
    class Config:
        orm_mode = True
        schema_extra = {
            'example':{
                'title':'Runing',
                'body':'Go for the runing'
            }
        }


class UserSchema(BaseModel):
    username : str
    email : str
    password : str

class UserModel(BaseModel):
    username : str
    email : str
    task : List[TaskModel]
    class Config:
        orm_mode=True

class Login(BaseModel):
    username : str
    password : str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None