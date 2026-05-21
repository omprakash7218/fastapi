from fastapi import FastAPI,HTTPException,status,Depends,Response,APIRouter
from fastapi.exception_handlers import http_exception_handler

from app.oauth2 import get_current_user # !
from ..database import  get_db
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
from typing import List


router = APIRouter(
    prefix = "/posts",
    tags=["POSTS"]
)
# ? GET ALL POST AT ONCE
#--------------------------------------------------------------------------------------------------------------
@router.get("/")
def get_post(db: Session= Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts
#--------------------------------------------------------------------------------------------------------------

# ? GET ALL POST BUT RESPONSE IS FILTERED FIRST 
#--------------------------------------------------------------------------------------------------------------
@router.get("/",response_model = List[schemas.Post_Response])
def show_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts
#--------------------------------------------------------------------------------------------------------------

# ? GET POST BY ID
#--------------------------------------------------------------------------------------------------------------
@router.get("/{id}")
def get_post(id:int,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"No post with id = {id}")
    return post
#--------------------------------------------------------------------------------------------------------------

# ? CREATE POST 
#--------------------------------------------------------------------------------------------------------------
@router.post("/",status_code=status.HTTP_201_CREATED,response_model = schemas.Post_Response)
def create_post(post:schemas.Post,db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)   # !
    return new_post
#--------------------------------------------------------------------------------------------------------------

# ? EDIT POST
# !
#--------------------------------------------------------------------------------------------------------------
@router.put("/{id}",status_code= status.HTTP_202_ACCEPTED,response_model = schemas.Post_Response)
def edit_post(id: int, post: schemas.Post,db: Session= Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    query_post = db.query(models.Post).filter(models.Post.id == id)
    existing_post = query_post.first()
    if existing_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"No post with id = {id}")
    query_post.update(post.dict(),synchronize_session = False)
    db.commit()
    return query_post.first()
#--------------------------------------------------------------------------------------------------------------

# ? Delete Post   
# !
#--------------------------------------------------------------------------------------------------------------
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    query_post= db.query(models.Post).filter(models.Post.id == id)
    if query_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Looks like you have entered an invalide id({id})")
    query_post.delete(synchronize_session= False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------------------------