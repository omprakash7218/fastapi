from .database import Base
from sqlalchemy.sql.expression import null
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
class Postr(Base):
    __tablename__="revposts"
    id = Column(Integer,primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean , server_default ='TRUE',nullable=False)

#------------------------------------------------------

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key =True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String,nullable = False)
    published = Column(Boolean,server_default='TRUE',nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default = text('NOW()'))


# ! START phase 2!!
# ? Handling user registration
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key = True, nullable = False)
    email = Column(String,nullable = False , unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default = text('NOW()'))

