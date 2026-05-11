#
from . import utils
#
import time
from typing import List
from fastapi import FastAPI,HTTPException,Response 
from fastapi import status
from typing import Optional
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
#--------------------------------------------------
# ? SQLAlchemy
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db,engine
from . import models , schemas

models.Base.metadata.create_all(bind=engine)

#--------------------------------------------------
# ? PSYCOPG2
try:
    conn = psycopg2.connect(host = "localhost",database = "fastapi",user="postgres",password="password123",cursor_factory=RealDictCursor)
    cur = conn.cursor()
    print("Database connection was successful!!")
except Exception as error:
    print("Connection to database has failed.")
    print(f"The error was: {error}")
    time.sleep(2)

app = FastAPI()

# @app.get("/")
# def get_post():
#     return{
#         "message": "Hey this is a new python file post postgres basics by Sanjeev Thiagranjan"
#     }
# --------------------------------------------------------
# ? PSYCOPG2
@app.get("/posts")
def show_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    print(posts)
    return {
        "message":posts
    }

# ? SQLALCHEMY
@app.get("/sqlalchemy",response_model= List[schemas.Post_Response])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts



# ---------------------------------------------------------




#-----------------------------------------------------------
# ?PSYCOPG2
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post : schemas.PostCreate ):
    cur.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) returning *""",(post.title,post.content,post.published) )
    new_post = cur.fetchone()
    print(new_post)
    conn.commit()
    return {
        "Your post":f"Your post has been created. {new_post}"
    }

# ? SQLALCHEMY
# class Post(BaseModel):
#     title:str
#     content:str
#     published:bool= True
@app.post("/postsalc",status_code=status.HTTP_201_CREATED,response_model=schemas.Post_Response)
def create_post(post: schemas.PostCreate, db:Session=Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
#---------------------------------------------------------------------------------



#---------------------------------------------------------------------------------
# ? PSYCOPG2
@app.get("/posts/{id}")
def get_post_id(id:int):
    cur.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    post_id = cur.fetchone()
    if not post_id :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= "The post does not exist in the database, sorry!")
    return {
        "message": post_id
    }

# ? SQLALCHMEY
@app.get("/postsql/{id}",response_model=schemas.Post_Response)
def show_post(id = int, db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "Post does not exist.")
    return post
#---------------------------------------------------------------------------------



#---------------------------------------------------------------------------------
# ? PSYCOPG2
@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cur.execute("""Delete  from posts where id = %s returning *""",(str(id),))
    deleted_post = cur.fetchone()
    conn.commit()
    if  deleted_post==None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail = "There is no post with the id given.")
    return Response(status_code = status.HTTP_204_NO_CONTENT)

# ? SQLALCHMEY
@app.delete("postsql/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # ?  post_query = db.query(models.Post).filter(models.Post.id== id).first()  # this is a command which points to the actual post if it exist
    post_query = db.query(models.Post).filter(models.Post.id==id)       # this is distinct. it is a query not the actual post
    if post_query.first() == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "Post doesnot exists int he first place!")
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
#---------------------------------------------------------------------------------



#---------------------------------------------------------------------------------
# ? PSYCOPG2
@app.put("/posts/{id}")
def update_post(id:int,post:schemas.PostCreate):
    cur.execute("""update posts set title = %s,content = %s,published =%s where id = %s returning * """,(post.title,post.content,post.published,str(id),))
    updated_post = cur.fetchone()
    conn.commit()
    if updated_post ==None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail = "There is no post with the given id.")
    return {
        "message":updated_post
    }


# ? SQLALCHEMY
@app.put("/postsql/{id}",response_model = schemas.Post_Response)
def update_post(id:int , post:schemas.PostCreate, db: Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    if existing_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "There is no post with the given id.")
    post_query.update(post.dict(),synchronize_session = False)
    db.commit()
    # return existing_post # !
    return post_query.first() 


# !-------------------------------------
# !-------------------------------------
# !-------------------------------------
# !-------------------------------------
# !-------------------------------------
# !-------------------------------------
# Next part of the backend development is staring
# Path operation for creating a new user 

# ? pydantic model for this specific user route
# ? from schemas

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






















