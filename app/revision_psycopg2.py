from fastapi import FastAPI,status,HTTPException,Response
import json
import time
import psycopg2
from psycopg2.extras import RealDictCursor, NamedTupleCursor, DictCursor
from pydantic import BaseModel
from fastapi import Body
app = FastAPI()
class Post(BaseModel):
    title:str
    content:str
    published: bool = True
try:
    conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="password123",cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print("connecting to the database......")
    time.sleep(2)
    print("Connected Successfully!")
except Exception as error:
    print("connecting to the database.....")
    time.sleep(2)
    print("Connection to the database failed.")
    print("Exception: ",error)
    time.sleep(2)
@app.get("/")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    # json_data = json.dumps(posts)

    return {
        # "posts":json_data
        "posts":posts
    }
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) returning *""",(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    print(new_post)
    conn.commit()
    return {
        "updates":new_post
    }
@app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute('''DELETE FROM posts where id = %s RETURNING*''',(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "The id is not available to be deleted.")
    return Response(status_code= status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
def edit_post(post:Post,id:int):
    cursor.execute("""UPDATE posts SET title=%s,content=%s where id = %s RETURNING *""",(post.title,post.content,str(id)))
    updated_post = cursor.fetchone()
    print(updated_post)
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The post you are trying to edit does not exist.")
    return{
        'Updated Post':updated_post
    }