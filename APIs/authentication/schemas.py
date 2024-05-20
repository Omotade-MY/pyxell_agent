from pydantic import BaseModel

class User(BaseModel):
    userid: str
    username: str
    password: str
    session_token: None|str 

class Session(BaseModel):
    userid: str
    token: str

class Bool(BaseModel):
    response: bool