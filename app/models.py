from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean
from .database import Base 


class Post(Base): 
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)#nullable is the equivalent of not null in a sql database
    title = Column(String, nullable=False)
    content = Column (String, nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), 
                            nullable=False, server_default=text('now()')) #to set the default timestamp to the current one 