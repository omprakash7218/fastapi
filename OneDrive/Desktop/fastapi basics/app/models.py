from .database import Base

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.sql.expression import null 
from sqlalchemy import String
from sqlalchemy import Boolean

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key =True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String,nullable = False)
    published = Column(Boolean,default=True)