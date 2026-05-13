from fastapi import FastAPI, Depends, HTTPException,status,Response
from .database import engine,get_db
from sqlalchemy.orm import Session
from . import models,utils,schemas
from .routers import auth, post,user
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)