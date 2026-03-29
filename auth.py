from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
import hashlib
from fastapi import HTTPException     

SECRET_KEY = "SECRET123"  #These two (secret_key,algo) do encoding and decoding of our password
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES =  60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: int, role: str, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES ) 
    payload = {
        "sub": str(user_id),  
        "user_id": user_id,
        "role": role,
        "exp": expire
    } 
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# def create_access_token(
#     user,
#     expires_delta: Optional[timedelta] = None
# ):
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

#     payload = {
#         "sub": str(user.id),  
#         "exp": expire
#     }
#     token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#     return token  


   