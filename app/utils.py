from passlib.context import CryptContext

pwd_context = CryptContext(schemes= ["bcrypt"], deprecated="auto") #this tells fast api what the deafult hashing algorithm is

def hash(password: str):
    return pwd_context.hash(password)