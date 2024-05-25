
from typing import Annotated
from authentication.auth import authorize_user, hash_password, create_access_token, verify_token
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from authentication.schemas import User, Bool, Token
from typing import Annotated
from utils.db_utils import init_db, get_user, add_new_user

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

app = FastAPI(title="PyxellAI")
app.include_router

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # You can specify allowed methods like ["GET", "POST"]
    allow_headers=["*"],  # You can specify allowed headers like ["Content-Type", "Authorization"]
)

async def get_current_user(token: Annotated[Token, Depends(oauth2_scheme)]):

    print("Got here!!!", type(token))
    payload = verify_token(token)
    return payload

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



@app.post("/login", response_model=Token)
async def login(credentials: Annotated[OAuth2PasswordRequestForm,  Depends()]):
    print("called")
    user = get_user(credentials.username)
    #if user and verify_password(credentials.password, user.password):
    if user:
        authorize_user(credentials.username, credentials.password)
        token_data = {"sub": user.username}
        access_token = create_access_token(data=token_data)
        #update_session(login_token=access_token)
        
        return {"token": access_token, "token_type": "bearer"}
    
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    

@app.post("/users/me")
async def query(user: Annotated[User,  Depends(get_current_user)]):
    return {'response':f"Hello {user.username} is Logged In"}
