from fastapi import HTTPException,status,Response,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas,utils,models
from typing import List
from .. import oauth2
# ? Add user into the db
router = APIRouter(
    prefix = "/users",
    tags = ["USERS"]
)
# ? Get all users 
@router.get("/",response_model=List[schemas.UserOut],status_code = status.HTTP_202_ACCEPTED)
def get_users(db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users

# ? Create new user with hashed password
@router.post("/",status_code = status.HTTP_201_CREATED,response_model= schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ? Get User using id.
@router.get('/{id}',response_model = schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user)):
    print("Requestd by:",current_user.email)
    user = db.query(models.User).filter(models.User.id == id ).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail = f"The user with id:{id} does not exist in the database.")
    if current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not an authorized user.")
    return user
