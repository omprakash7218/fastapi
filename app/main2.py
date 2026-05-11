
# ? I learning fastapi and backend from Sanjeev Thiyagrajan yt channel. 
# ? I am on the 15/100 video, I needed a fresh python file to carry on with the topics.
# ! So here we are.


from fastapi import FastAPI
from typing import Optional
import math
from pydantic import BaseModel
from fastapi import Response
from fastapi import status
from fastapi import HTTPException


class Statuscode201(BaseModel):
    message: str

lst = [{"Asian":"Exterior - Ace,Apex","id":1},{"Asian":"Interior - Tractor,Premimium,Royale","id":2}]
def find_details(id):
    for items in lst:
        if items["id"]==id:
            return items


app = FastAPI()


@app.get("/details/{id}")     # ? This is a decorator   {id} this is a path parameter
def get_details(id: int, response: Response):

    detail = find_details(id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Detail with id {id} was not found!")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message":f"Detail with id {id} was not found!"}
    return {
        "details":detail
    }
@app.get("/details/latest")    # ! fast api is going to check for the match from top to bottom.
                               # ! It going to get matched with @app.get("/details/{id}")  {id} can be a string.
                               # ! We need to be very careful . take this route above the previous matched one.
def get_latest_post():
    print(lst[len(lst)-1])

@app.post("/change_default_status_code",status_code=status.HTTP_201_CREATED)
def creating_with_statuscode201(create: Statuscode201):
    return {
                "message":create
    }

