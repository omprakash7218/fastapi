
from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

def root():
    return {"message": "Welcome to my api !!!!!"} 


my_posts = [{
                "Name":"Omprakash Chaudhary",
                "Work": "BBA student at shoolini universtity",
                "Experience":"No experience as a CS grad but have managed a shop in his home town.",
                "id": 1
            },
            {
                "Interest":"Loves playing cricket and watching a cricket match, playing vr and intense games using ps5 or hardcore pc",
                "Skills": "Knows python basics,sql intermediate,tablue basics,excel basics",
                "Achievements": "Good at academics but no achievements as of yet. Tata genAI certified and couple of certification in MySql from congnative classes(IBM)",
                "id":2,
                "who's listening on the port 8000":"netstat -ano | findstr :8000",
                "kill listener": "taskkill /PID <id_of_the_listener> /F"
            }]

@app.get("/posts")
def get_posts():
    return {
        "my_posts":my_posts,
        "data":"This is your post",
        "hemant":"Ompraksh chaudhary ka bhai"
    }

@app.get("/credentials")
def get_credentials():
    return{
            "My Name":"Omprakash Chaudhary",
            "Class": "Third Semester BBA Student",
            "University":"Shoolini University",
            "Work experience": "A manager and VLE"
        }
@app.post("/post")
def create_post(new_post: Post):
    # print(new_post.dict())
    # print(new_post.model_dump())
    post_dict = new_post.dict()
    post_dict["id"]=randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": new_post.dict()}

# title str , content str

 # ! so this is actually a pydantic model we change it to dictionary