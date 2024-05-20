
from typing import Annotated
from authentication.auth import hash_password, verify_password, create_access_token, verify_token
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from authentication.schemas import User, Bool

from utils.db_utils import init_db, get_user, add_new_user, update_session

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI(title="PyxellAI")

async def get_current_user(user: Annotated[str, Depends(security)]):

    #print("Got here!!!", token)
    #payload = verify_token(token)
    return user

@app.post("/register")
async def register_user(username, password, confirm_password):
    init_db()
    user = get_user(username)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        try:
            assert password == confirm_password
            add_new_user(username, hash_password(password))
        except AssertionError:
            raise HTTPException(status_code=400, detail="password and confirm password do not match")



@app.post("/login/")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user(credentials.username)
    if user and verify_password(credentials.password, user.password):
        token_data = {"sub": user.username}
        access_token = create_access_token(data=token_data)
        update_session(user.userid, login_token=access_token)
        return {"access_token": access_token, "token_type": "bearer"}
    
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    

@app.post("/users/me")
async def query(current_user: Annotated[User,  Depends(get_current_user)]):
    return {'response':f"Hello {current_user.username} is Logged In"}