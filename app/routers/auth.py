from fastapi import FastAPI,Depends,HTTPException,APIRouter,status
from .. import database,models,schemas, utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login")
def login(user_credentials=Depends(OAuth2PasswordRequestForm),   db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email== user_credentials.username).first()
    if not user: 
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail= "Invalid Credentials")
    if utils.verify(user_credentials.password, user.password)==False:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail= "Invalid Credentials")
    token = oauth2.create_access_token({"user_id":user.id})

    return {"Access Token":token,"Token Type":"bearer"}


# @router.post("/login")
# def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.email==user_credentials.username).first()
#     if not user:
#         raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail="Invalid credentials") 
#     if not utils.verify(user_credentials.password,user.password):
#         raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
#     access_token = oauth2.create_access_token({"user_id":user.id})
#     return {"Access Token : ":access_token,"Token Type":"bearer"}