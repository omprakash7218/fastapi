# from fastapi import FastAPI
# from pydantic import BaseModel


# app = FastAPI()

# class Item(BaseModel):
#     name: str
#     price: float
# @app.get("/")
# def root():
#     return {"message":"Welcome to my firt backend learning revision."}

# @app.get("/read")
# def get_read():
#     return {"message":"The get function is used to read only. User sends request to us we provide the user with info or data."}

# @app.post("/items")
# def create_item(item:Item):
#     return {
#         "message":"Item recieved!",
#          "item": item.dict() 
#         }

from typing import Optional
from random import randrange
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.params import Body

app = FastAPI()

# This is your blueprint — what JSON you expect to receive
class Item(BaseModel):
    name: str
    price: float
    type: Optional[str] = None
    rating: Optional[int] = None
@app.post("/items")
def create_item(item: Item):
    print(item.dict().items())
    return {
        "message": "Item received!",
        "item": item.dict()

    }

@app.post("/posts")
def create_post( payload: dict = Body(...)):
    print(type(payload))
    print(payload)
    for I in payload.items():
        print(I[0])
  
    return {
        "message" : " Hello world! This is my first post method"
    }
class Details(BaseModel):
    user_id:str
    password:str

login_list = [{"id":1,"username":"omg311","password":"xyz@321"}]
@app.post("/users")
def user_credentials(login_details:Details):
    login_details_dict = login_details.dict()
    login_details_dict["id"]=randrange(0,1110010101010)
    login_list.append(login_details_dict)
    print(login_list)
    return login_details.dict()

@app.get("/users")
def user_credentials():
    return {"login_list":login_list}