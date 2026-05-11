import psycopg2
from fastapi import FastAPI, HTTPException, Response,status
from .. import schemas
import time
from psycopg2.extras import RealDictCursor

try: 
    conn = psycopg2.connect(host= "localhost",user= "postgres",database="fastapi",password = "password123",cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connection established.")
except Exception as error:
    print("Connection failed.")
    print(f"Error: {error}")

app = FastAPI()

# ? Get posts
@app.get("/posts")
def show_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts

# ? Get a Post
@app.get("/posts/{id}")
def show_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= "Sorry dude! No luck. There is no post with this particualr id.")
    return post

# ? Create Posts 
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post

# ? Edit post
@app.put("/posts/{id}",status_code = status.HTTP_202_ACCEPTED)
def update_post(id: int,post:schemas.Post):
    cursor.execute("""UPDATE posts SET title = %s,content = %s, published= %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post==None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail = "Post not found.")
    return updated_post

# Delete a post 
@app.delete("/posts/{id}",status_code = status.HTTP_202_ACCEPTED)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="No post with this particular id. Please enter a valid one.")
    return Response(status_code = status.HTTP_204_NO_CONTENT)