from fastapi import FastAPI
from fastapi.param_functions import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Hello world"}

@app.get("/posts")
def get_posts():
    return{'data': "This is your posts"}


@app.post('/create_post')
def create_post(payload: dict = Body(...)): 
    #going to extract all the fields from the body and convert it into a python dictionary and then store it inside the variable payload  
    print(payload)
    return{"new_post": f"title {payload['title']} content: {payload['content']}"} #to retreive the raw posts