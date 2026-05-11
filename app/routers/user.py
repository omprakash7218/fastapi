from .. import schemas,utils,models
from fastapi import FastAPI,HTTPException,status,Response,Depends
from ..database import get_db
from sqlalchemy.orm import Session


app = FastAPI()
@app.post("/users",status_code = status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    # hash the password - user.password
    try:
        clean_password = user.password.strip()[:72]
        hash_password = utils.hashed_password(clean_password)
        print("Password repr:", repr(user.password))
        print("Byte length:", len(user.password.encode("utf-8")))

        user.password = hash_password

        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))




@app.get('/users/{id}',response_model = schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id ).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail = f"The user with id:{id} does not exist in the database.")
    return user
