import time
from fastapi import FastAPI,HTTPException,Response 
from fastapi import status
from typing import Optional
from pydantic import BaseModel
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
app = FastAPI()
@app.get("/")
def get_post():
    return{
        "message": "Hey this is a new python file post postgres basics by Sanjeev Thiagranjan"
    }

class Post(BaseModel):
    title : str
    content : str
    published : bool = True

try:
    conn = psycopg2.connect(host = "localhost",database = "fastapi",user="postgres",password="password123",cursor_factory=RealDictCursor)
    cur = conn.cursor()
    print("Database connection was successful!!")
    

except Exception as error:
    print("Connection to database has failed.")
    print(f"The error was: {error}")
    time.sleep(2)



@app.get("/posts")
def show_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    print(posts)
    return {
        "message":posts
    }

@app.get("/posts/{id}")
def get_post_id(id:int):
    cur.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    post_id = cur.fetchone()
    if not post_id :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= "The post does not exist in the database, sorry!")
    return {
        "message": post_id
    }

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    cur.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) returning *""",(post.title,post.content,post.published) )
    new_post = cur.fetchone()
    print(new_post)
    conn.commit()
    return {
        "Your post":f"Your post has been created. {new_post}"
    }
@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cur.execute("""Delete  from posts where id = %s returning *""",(str(id),))
    deleted_post = cur.fetchone()
    conn.commit()
    if  deleted_post==None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail = "There is no post with the id given.")
    return Response(status_code = status.HTTP_204_NO_CONTENT)
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cur.execute("""update posts set title = %s,content = %s,published =%s where id = %s returning * """,(post.title,post.content,post.published,str(id),))
    updated_post = cur.fetchone()
    conn.commit()
    if updated_post ==None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail = "There is no post with the give id.")
    return {
        "message":updated_post
    }
