from pydantic import BaseModel
from typing import Optional #this is to enable more complex field types
from random import  randrange #to import a random integer

class Product(BaseModel):
    title: str
    description: str
    price: int
    ratings: Optional[int] = None
    published: Optional[bool]= True 
    id: Optional[int]= None 

data = {
    "title": "Iphone 13 pro max",
    "description": "This is the latest Iphone from apple",
    "price": 1000, 
    "ratings": 4.56,
    "id": randrange(0, 100000000) #creates a random integer between 0 and 100000000
}

product = Product(**data) #to read the python dictionary

print(product)