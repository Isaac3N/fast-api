from typing import Optional
from fastapi import FastAPI, Response, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import  randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time 
from sqlalchemy.orm import Session
from . import models 
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine) #for connecting to the database

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel): #this is an extended base model using pydantic 
    title: str
    content: str
    published: bool = True 
    rating: Optional[int] = None # for integers
    id: Optional[int]=None

#code for connecting to the database 
while True: 
    try: 
        conn = psycopg2.connect(host="localhost", database="fastapi", 
        user="postgres", password= "vendremecca123", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break 
    except Exception as error: 
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)# to set a time until it  reconnects 


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
            return i


@app.get("/")
async def root():
    return {"message" : "Hello world"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all() # to get all the queried posts from a db table called Post 
    return {"data": posts} #--> dummy database success routes 

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")# to retreive all posts from our database 
    # posts=cursor.fetchall() --> This is how to retrieve a post using RAW SQL 
    posts = db.query(models.Post).all()
    print(posts)
    return{'data': posts}


@app.post('/posts')
def create_posts(post: Post): 
    #going to extract all the fields from the body and convert it into a python dictionary and then store it inside the variable payload  
    # %s is a way of passing parameters to a SQL statement, and passing a sequence of values as the second argument of the function
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s ) RETURNING *""", 
        (post.title, post.content, post.published)) # order those matter 
    # post_dict=  post.dict()#convert the Post class to a dixtionary 
    # post_dict['id'] = randrange(0, 100000000) #creates a random integer of
    # my_posts.append(post_dict)
    new_post = cursor.fetchone()  
    conn.commit()
    return{"data": new_post} #to retreive the raw posts

# title str, content str

@app.get("/posts/{id}") #to retrieve the information from the path
def get_post(id:int): #to convert the id into an integer
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post=cursor.fetchone()
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
    cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", (str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f"post with id: {id} does not exist" )

    my_posts.pop(deleted_post)
  
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    cursor.execute("""UPDATE posts SET title= %s, content = %s, published = %s WHERE id = %s 
        RETURNING *""", 
            (post.title, post.content, post.published, (str(id))))
    updated_post=cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f"post with id: {id} does not exist" )
    return {"data": updated_post}
 