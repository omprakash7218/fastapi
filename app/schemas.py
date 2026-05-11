from datetime import datetime 
from pydantic import EmailStr
from pydantic import BaseModel,constr



class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# ? Now we are going to learn about responses from the server.
class Post_Response(PostBase):
    id:int
    class Config:
        orm_mode = True

# Fablue Stuffed Bamboo Panda Plush Toy | White & Black Panda with Green Bag | Gift for Boys & Girls
# class UserCreate(BaseModel):
#     email: EmailStr
#     password: constr(min_length = 8, max_length = 72)
from pydantic import BaseModel, constr

class UserCreate(BaseModel):
    email: str
    password: constr(min_length=8, max_length=72)

class UserOut(BaseModel):
    email: EmailStr
    id:int
    created_at: datetime
    class config:
        orm_mode = True