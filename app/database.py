from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from time import sleep
import psycopg2
from psycopg2.extras import RealDictCursor
from . config import settings


# SQLALCHEMY_DATABASE_URL = 'POSTGRESQL://<username>:<password>@<ipaddress-or-hostname>/<database name>
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)
Base = declarative_base()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# try: 
#     conn = psycopg2.connect(host= "localhost",user= "postgres",database="fastapi",password = "password123",cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Connection established.")
# except Exception as error:
#     print("Connection failed.")
#     print(f"Error: {error}")
#     time.sleep(2)