from sqlite3 import Date
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Post(BaseModel): #this is an extended base model using pydantic 
    title: str
    content: str
    published: bool = True 
    #rating: Optional[int] = None # for integers
    id: Optional[int]=None

class PostBase(BaseModel):
    title: str 
    content: str 
    published: bool = True 

class PostCreate(PostBase): #inheriting all the objects in the postbase class 
    pass 

class Post(PostBase):
    id: int
    created_at: datetime 

class Config:
    orm_mode = True 

class UserCreate(BaseModel):
    email: EmailStr
    password: str 

#Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, 
# but an ORM model (or any other arbitrary object with attributes).    

# class CreatePost(BaseModel): #schema for created post
#     title: str 
#     content: str 
#     published: bool = True 

# class UpdatePost(BaseModel): #schema for updated post 
#     title: str 
#     content: str 
#     published: bool 
