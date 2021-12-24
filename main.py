from typing import Optional
from fastapi import FastAPI
from fastapi.param_functions import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True 
    rating: Optional[int] = None 

@app.get("/")
async def root():
    return {"message" : "Hello world"}

@app.get("/posts")
def get_posts():
    return{'data': "This is your posts"}


@app.post('/create_post')
def create_post(new_post: Post): 
    #going to extract all the fields from the body and convert it into a python dictionary and then store it inside the variable payload  
    print(new_post.title)
    return{"data": "new post"} #to retreive the raw posts

# title str, content str