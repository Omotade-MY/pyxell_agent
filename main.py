
from typing import Annotated
from server.authentication.auth import authorize_user, hash_password, create_access_token, verify_token
from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from server.authentication.schemas import User, Bool, Token
from typing import Annotated
from server.utils.db_utils import init_db, get_user, add_new_user
from functools import cache

@cache
def create_agent():
    import openai
    import os
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    from agents.browser_agent import web_agent as wgt
    bagent = wgt.BrowserAgent()
    return bagent

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

app = FastAPI(title="PyxellAI")

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
async def register_user(username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    init_db()
    user = get_user(username)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        add_new_user(username, hash_password(password))
    return {"detail": "User registered successfully"}




@app.post("/login", response_model=Token)
async def login(credentials: Annotated[OAuth2PasswordRequestForm,  Depends()]):
    print("called")
    user = get_user(credentials.username)
    #if user and verify_password(credentials.password, user.password):
    if user:
        authorize_user(credentials.username, credentials.password)
        token_data = {"sub": user.username}
        access_token = create_access_token(data=token_data)
        
        return {"token": access_token, "token_type": "bearer"}
    
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
@app.post("/chat/")
async def get_response(user: Annotated[User,  Depends(get_current_user)], bagent = Depends(create_agent), prompt: str = Form(...)):
    print("Entering Web Agent Execution")
    response = bagent.execute(prompt)
    #return {'response':f"Hello Welcome to PyxellAI! How can I help you.\n\n We got the below message <{prompt}>"}
    return {'response': response}

@app.post("/users/me")
async def query(user: Annotated[User,  Depends(get_current_user)]):
    
    return {'response':f"Hello {user['sub']} is Logged In"}
