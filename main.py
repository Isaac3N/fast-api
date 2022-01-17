from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.exceptions import HTTPException 
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import  randrange

app = FastAPI()


class Post(BaseModel): #this is an extended base model using pydantic 
    title: str
    content: str
    published: bool = True 
    rating: Optional[int] = None # for integers
    id: Optional[int]=None

my_posts = [
         {
            "title": "title of post 1",
            "content": "content of post 1", 
            "id": 1,

        }, 
        {
            "title": "favorite foods", 
            "content": "I like pizza",
            "id": 2, 
        },
]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p
#logic to find the id 

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return p


@app.get("/")
async def root():
    return {"message" : "Hello world"}

@app.get("/posts")
def get_posts():
    return{'data': my_posts}


@app.post('/posts')
def create_posts(post: Post): 
    #going to extract all the fields from the body and convert it into a python dictionary and then store it inside the variable payload  

    post_dict=  post.dict()#convert the Post class to a dixtionary 
    post_dict['id'] = randrange(0, 100000000) #creates a random integer of
    my_posts.append(post_dict)
    return{"data": post_dict} #to retreive the raw posts

# title str, content str

@app.get("/posts/{id}") #to retrieve the information from the path
def get_post(id:int, response: Response): #to convert the id into an integer
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"post with the id {id} not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with the id {id} not found."}
    return(post)

@app.delete("/posts/{id}")
def delete_post(id:int):
    #deleting a post
    #find the index in the array that has required id 
    index = find_index_post(id)
    my_posts.pop(index)
    return{"message": "The post was sucessfully deleted"}
