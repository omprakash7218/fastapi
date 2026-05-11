from fastapi import FastAPI
from fastapi.params import Body
from fastapi import Depends    # !

from pydantic import BaseModel

import psycopg2

from .database import engine
from .database import get_db   # !

from sqlalchemy.orm import Session  # !

from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def show_post():
    return {
        "message1":"Looks like we have to make all of the methods again for the brand new main5 file.",
        "message2":"Man! it sucks. But hey! can't say I am sad about it, when I am getting revise all of these topics again."
    }

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {
        "status": "success"
    }