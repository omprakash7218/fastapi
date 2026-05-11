from typing import Optional
from fastapi import FastAPI,status,HTTPException,Response
from pydantic import BaseModel
from fastapi.params import Body
from sentry_sdk import HttpTransport
app = FastAPI()
class Posts(BaseModel):     #! This schema will be used to update the post(method) also.
    name: str
    about: str
    age: Optional[int] = None
lst = [{"name":"Omprakash Chaudhry","id":1},{"class":12,"id":2},{"school":"DAV","id":3}]
# @app.get("/")
# def allpost():
#     return{
#                 "Posts":lst
#     }
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_1st_post(posts:Posts):
    return {
                "message":"Congratulations! you have made your very first post on our platform",
                "Your post":posts
    }
def find_dict(id):
    for i in lst:
        if i["id"] == id:
            return i

@app.get("/delete_a_post_id/{id}")
def delete_a_post(id:int):
    to_be_deleted = find_dict(id)
    if not to_be_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Detail with id {id} was not found!")
    return{
                "message": f"Here is your post: {to_be_deleted}"
    }
@app.post("/deleting_a_post",status_code=status.HTTP_201_CREATED)
def delete_post():
    return {
                "message":"Your soon to be deleted post is ready."
    }
def find_index_post(id):
    for index,item in enumerate(lst):
        if item["id"]==id:
            return index
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # deleting_post
    # find the inde in the array that has required ID
    # my_post.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} does not exist")
    lst.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@app.get("/")
def allpost():
    return{
            "Posts":lst
    }
@app.delete("/postss/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id : int):
    # logic for deleting a post
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Post with this id does not exist")
    lst.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@app.put("/posts/{id}")
def update_post(id: int , update: Posts):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"The post with id: {id} does not exist.")
    update_dict = update.dict()
    update_dict['id']= id
    lst[index] = update_dict    
    print(update)
    return {'message': update_dict}