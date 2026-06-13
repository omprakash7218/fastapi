from jose import JWTError , jwt
from datetime import datetime,timedelta
from . import schemas,models,database
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
from . config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
SECRET_KEY = settings.secret_key
#ALGORITHM 
ALGORITHM = settings.algorithm
#EXPIRATION_TIME
ACCESS_TOKEN_EXPIRY_MINUTES = settings.access_token_expire_minutes


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp":expire})
    access_token = jwt.encode(to_encode ,SECRET_KEY,algorithm=ALGORITHM)
    print("secret Key:",settings.secret_key)
    return access_token
                        

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    credentials_exception= HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid Credentials",headers= {"www-Authenticate":"Bearer"})
    token_data = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user :
        raise credentials_exception

    return schemas.UserOut.model_validate(user)


# def verify(token:str,credentials_exception):
#     try:
#         payload = jwt.decode(token,SECRET_KEY , algorithms=[ALGORITHM])
#         id:int = payload.get("user_id")
#         if id is None :
#             raise credentials_exception
#         token_data= schemas.TokenData(id = id)
#     except JWTError:
#         raise credentials_exception
#     print(token_data)
#     return token_data
    
# def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
#     credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",headers={"www-Authenticate":"Bearer"})
#     token = verify(token,credentials_exception)
#     user= db.query(models.User).filter(models.User.id==token.id).first()
#     return user