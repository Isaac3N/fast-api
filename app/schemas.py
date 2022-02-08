from pydantic import BaseModel
from typing import Optional

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

class Post(BaseModel):
    title: str 
    content: str 
    published: bool


# class CreatePost(BaseModel): #schema for created post
#     title: str 
#     content: str 
#     published: bool = True 

# class UpdatePost(BaseModel): #schema for updated post 
#     title: str 
#     content: str 
#     published: bool 
