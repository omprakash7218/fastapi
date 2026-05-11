from fastapi import FastAPI,status,HTTPException,Depends,Response
from sqlalchemy.orm import  Session
from . import models
from pydantic import BaseModel
import psycopg2
from .database import engine,get_db


models.Base.metadata.createall(bind = engine)

app = FastAPI()

class Post(BaseModel):
    title: str 
    content: str
    published: bool = True
@app.get("/sqlalchmey")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Postr).all()
    return {"message":posts}

@app.post("/sqlalchemy")
def add_post(post:Post,db: Session = Depends(get_db))