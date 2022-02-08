from pydantic import BaseModel
from typing import Optional

class Post(BaseModel): #this is an extended base model using pydantic 
    title: str
    content: str
    published: bool = True 
    #rating: Optional[int] = None # for integers
    id: Optional[int]=None