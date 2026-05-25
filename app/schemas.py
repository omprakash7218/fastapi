from datetime import datetime 
from pydantic import EmailStr
from pydantic import BaseModel,constr
from typing import Optional

class UserOut(BaseModel):
    email: EmailStr
    id:int
    created_at: datetime
    class Config:
        from_attributes = True

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    owner : UserOut

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True



class PostCreate(PostBase):
    pass
    

# ? Now we are going to learn about responses from the server.
class Post_Response(PostBase):
    id:int
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True

# Fablue Stuffed Bamboo Panda Plush Toy | White & Black Panda with Green Bag | Gift for Boys & Girls
# class UserCreate(BaseModel):
#     email: EmailStr
#     password: constr(min_length = 8, max_length = 72)
from pydantic import BaseModel, constr

class UserCreate(BaseModel):
    email: str
    password: constr(min_length=8, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int]=None
