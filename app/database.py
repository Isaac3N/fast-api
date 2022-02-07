from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = "postgresql://<postgres>:<vendremecca123>@localhost/fastapi"


engine = create_engine(SQLALCHEMY_DATABASE_URL) #the engine is what is reponsible for connecting the ORM to a sql database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine ) #the session is what is responsible for talking to a sql database 

Base = declarative_base()