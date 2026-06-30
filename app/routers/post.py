from asyncio import Barrier

from fastapi import FastAPI,HTTPException,status,Depends,Response,APIRouter
from fastapi.exception_handlers import http_exception_handler
from typing import Optional

from app.oauth2 import get_current_user # !
from ..database import  get_db
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
from typing import List

from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags=["POSTS"]
)
# ? GET ALL POST AT ONCE
#--------------------------------------------------------------------------------------------------------------
# @router.get("/")
# def get_post(db: Session= Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user)):
#     posts = db.query(models.Post).all()
#     return posts
#--------------------------------------------------------------------------------------------------------------

# ? GET ALL POST BUT RESPONSE IS FILTERED FIRST 
#--------------------------------------------------------------------------------------------------------------
@router.get("/",response_model=List[schemas.LikeOut])
# @router.get("/")
def show_posts(db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user),limit: int = 100,skip: int = 0,search:Optional[str]=""):
    print(search)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post,func.count(models.Like.post_id).label("Likes")).join(models.Like, models.Post.id==models.Like.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    return results
# important words 
# %20 means space in the search bar
# for skip the no. of post  -- offset
# for  limiting no. of post == limit
#--------------------------------------------------------------------------------------------------------------

# ? GET POST BY ID
#--------------------------------------------------------------------------------------------------------------
@router.get("/{id}",response_model=schemas.LikeOut)
def get_post(id:int,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post,func.count(models.Like.post_id).label("Likes")).join(models.Like,models.Like.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"No post with id = {id}")
    
    print("Requested by: ",current_user.email)
    return post
#--------------------------------------------------------------------------------------------------------------

# ? CREATE POST 
#--------------------------------------------------------------------------------------------------------------
@router.post("/",status_code=status.HTTP_201_CREATED,response_model = schemas.Post)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)   # !
    return new_post
#--------------------------------------------------------------------------------------------------------------

# ? EDIT POSTd
# !
#--------------------------------------------------------------------------------------------------------------
@router.put("/{id}",status_code= status.HTTP_202_ACCEPTED,response_model = schemas.Post_Response)
def edit_post(id: int, post: schemas.PostCreate,db: Session= Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    query_post = db.query(models.Post).filter(models.Post.id == id)
    existing_post = query_post.first()
    if existing_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"No post with id = {id}")
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail="Unauthorized access")
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
    if query_post.first().owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail="Unauthorized Access")
    query_post.delete(synchronize_session= False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------
# what if i want to see all the post by a specific owner id 
# @router.get("/",response_model = List[schemas.Post_Response])
# def show_posts(db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user)):
#     print("Requested by: ",current_user.email)
#     posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
#     return posts