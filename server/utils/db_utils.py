from server.authentication.schemas import *

#from database import engine, SessionLocal
#import models
from sqlalchemy.orm import Session
import os

root = os.path.join(os.getcwd(),'server/')
print(root)

def init_db():
    try:
        os.mkdir(root+'database/')
    except FileExistsError:
        pass
    try:
        fp = open(root+"database/user_db.json")
        fp.close()
    except FileNotFoundError:
        fp = open(root+"database/user_db.json", "w")
        users = dict(users=[], sessions=[])
        json.dump(users, fp, indent=4)
        fp.close()


import json

def add_new_user(username, password):
    
    with open(root+'database/user_db.json', 'r+') as fp:
        data = json.load(fp)
        userid = f"user0{len(data['users'])}"
        user = User(userid=userid,username=username.lower(), password=password, session_token=None)
        data['users'].append(user.model_dump())
        fp.seek(0)
        json.dump(data, fp, indent=4)


def get_user(username):
    with open(root+'database/user_db.json', "r") as f:
        user_db = json.load(f)
        try:
            user = [user for user in user_db['users'] if user["username"] == username][0]
            return User(**user)
        except IndexError:
            return None
        
def update_session(userid, login_token):
    with open(root+'database/user_db.json', "r+") as fp:
        user_db = json.load(fp)
        session = Session(userid=userid, token=login_token)
        
        user_db['sessions'].append(session.model_dump())
        fp.seek(0)
        print("User DB",user_db)
        json.dump(user_db, fp, indent=4)