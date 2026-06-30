from dns.resolver import _original_gethostbyaddr
from fastapi import FastAPI
from .database import engine
from . import models,utils,schemas
from .routers import auth, post,user,like
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)   # ! this can be commented out because we are using alembic for creating and editing tables 
origins = ["https://www.google.com","https://www.youtube.com"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_headers= ["*"],
    allow_methods=["*"],
    allow_credentials= True
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

@app.get("/")
def Hello():
    return {"message":"Hello world , This website is maintained by Omprakash Chaudhary!!{well poorly😅}"}