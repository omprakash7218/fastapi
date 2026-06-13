from fastapi import FastAPI,status,HTTPException,Depends,Response,APIRouter
from ..database import get_db
from .. import models,config,oauth2,schemas,database
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/likes",
    tags=['LIKE']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like,db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {like.post_id} does not exist.")

    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id,models.Like.user_id == current_user.id)

    found_like = like_query.first()
    if (like.dir) == 1:
        
        if found_like:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail=f"User_id {current_user.id} has already liked the post {like.post_id}")
        
        new_like = models.Like(user_id = current_user.id,post_id = like.post_id)
        db.add(new_like)
        db.commit()
        return {"message":"successfully added like"}
    elif like.dir == 0:
        if not found_like:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail= "Like does not exist.")
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted like."}


