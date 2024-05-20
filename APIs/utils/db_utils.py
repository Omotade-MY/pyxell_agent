from authentication.schemas import *
from authentication.auth import hash_password, verify_token, verify_password
from fastapi import FastAPI, HTTPException, Depends, Header
import os



def init_db():
    try:
        os.mkdir('database/')
    except FileExistsError:
        pass
    try:
        fp = open("database/user_db.json")
        fp.close()
    except FileNotFoundError:
        fp = open("database/user_db.json", "w")
        users = dict(users=[], sessions=[])
        json.dump(users, fp, indent=4)
        fp.close()


import json

def add_new_user(username, password):
    
    with open('database/user_db.json', 'r+') as fp:
        data = json.load(fp)
        userid = f"user0{len(data['users'])}"
        user = User(userid=userid,username=username.lower(), password=password, session_token=None)
        data['users'].append(user.model_dump())
        fp.seek(0)
        json.dump(data, fp, indent=4)


def get_user(username):
    with open('database/user_db.json', "r") as f:
        user_db = json.load(f)
        try:
            user = [user for user in user_db['users'] if user["username"] == username][0]
            return User(**user)
        except IndexError:
            return None
        
def update_session(userid, login_token):
    with open('database/user_db.json', "r+") as fp:
        user_db = json.load(fp)
        session = Session(userid=userid, token=login_token)
        
        user_db['sessions'].append(session.model_dump())
        fp.seek(0)
        print("User DB",user_db)
        json.dump(user_db, fp, indent=4)

def get_token(user):
    user = get_user((user.username))
    if user and verify_password(user.password, user.password):
        userid = user.userid
        with open('database/user_db.json', "r") as fp:
            user_db = json.load(fp)
            sessions = user_db['sessions']
            token = [tok['token'] for tok in sessions if tok['userid']==userid][0]
        return token


