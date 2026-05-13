from fastapi import APIRouter,Depends,Response,HTTPException,status
from .. import database,utils,schemas,models
from sqlalchemy.orm import Session

router = APIRouter(
    tags =["LOGIN"]
)
@router.post("/login")
def authorization(user_credentials:schemas.UserLogin,db:Session=Depends(database.get_db)):
    user= db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Invalid Credentials")
    # create a token here and return it to the client web browser 
    return {"token":"here is your token"}
#$2b$12$.nEDKRCbLQeU229iddTvfu.0/RA1mcuohJXsNqdAWuUbYBLlE9zvi
#$2b$12$B3EFgZP1O2EzTHuyUioFweLTaJKlzpfzegExNaftO/d7/TYHAgQjS