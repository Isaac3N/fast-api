from typing import Optional, List
from fastapi import FastAPI, Response, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import  randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time 
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine) #for connecting to the database

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




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

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all() # to get all the queried posts from a db table called Post 
#     return {"data": posts} #--> dummy database success routes 

@app.get("/posts", response_model=List[schemas.Post])#to fetch a list of posts )
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")# to retreive all posts from our database 
    # posts=cursor.fetchall() --> This is how to retrieve a post using RAW SQL 
    posts = db.query(models.Post).all()
    print(posts)
    return posts 


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post) #the schema that the response should follow )
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db)): 
    #going to extract all the fields from the body and convert it into a python dictionary and then store it inside the variable payload  
    # %s is a way of passing parameters to a SQL statement, and passing a sequence of values as the second argument of the function
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s ) RETURNING *""", 
    #     (post.title, post.content, post.published)) # order those matter 
    # # post_dict=  post.dict()#convert the Post class to a dixtionary 
    # # post_dict['id'] = randrange(0, 100000000) #creates a random integer of
    # # my_posts.append(post_dict)
    # new_post = cursor.fetchone()  
    # conn.commit()
    # print(**post.dict()) #** is used to unpack a dictionary
    new_post = models.Post(**post.dict())
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published) #to create the posts 
    db.add(new_post) #to link the created posts to the database 
    db.commit() #to commit the chnages 
    db.refresh(new_post) #to get the underline code writtem by retrieving it 
    return new_post #to retreive the raw posts

# title str, content str

@app.get("/posts/{id}", response_model=schemas.Post) #to retrieve the information from the path
def get_post(id:int, db: Session = Depends(get_db)): #to convert the id into an integer
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post=cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first() #this is the equivalent of doing where in sql and then it finds the first instance and then returns that
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"post with the id {id} not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with the id {id} not found."}
    return(post)

@app.delete("/posts/{id}")
def delete_post(id:int, db: Session = Depends(get_db)):
    #deleting a post
    #find the index in the array that has required id 
    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", (str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f"post with id: {id} does not exist" )

    post.delete(synchronize_session=False)
    db.commit()
  
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title= %s, content = %s, published = %s WHERE id = %s 
    #     RETURNING *""", 
    #         (post.title, post.content, post.published, (str(id))))
    # updated_post=cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id )

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail= f"post with id: {id} does not exist" )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


#anytime you need a path operation to work with the database you need to copy db: Session = Depends(get_db) this into the argument
 

#creating a user 
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash the password - user.password 
    hashed_password = utils.hash(user.password) #to hash the password 
    user.password  = hashed_password 

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 
    
