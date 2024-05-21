import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, Header
from utils.db_utils import get_user

#from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#from fastapi import Depends, HTTPException, APIRouter
#from authentication.schemas import User, Bool, Token
#from typing import Annotated


#URL_PREFIX = "/auth"

#router =  APIRouter(prefix = URL_PREFIX)

#oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/auth/token")

#@router.post("/token")

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


SECRET_KEY = "jwt-secret-key-testing@access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def authorize_user(username, password):
    user = get_user(username)
    if user and verify_password(password, user.password):
        return user
    else:
        return False
