from passlib.context import CryptContext   # !

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")        # !
def hashed_password(password:str):
    return pwd_context.hash(password)

def veri(fresh_password,hashed_password):
    return pwd_context.verify(fresh_password,hashed_password)
from random import random
from string import ascii_letters
print(ascii_letters)
from digits import 