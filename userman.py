import json
import bcrypt
import random

def hash(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed


def isAdmin(password, hashed):
    password = password.encode('utf-8')
    hashed = hashed.encode('utf-8')
    isAdmin = bcrypt.checkpw(password, hashed)
    return isAdmin


def load_users(filename):
    file = open(filename)
    data = json.load(file)
    file.close()
    return data


def login(username, password):
    for i in load_users("admins.json"):
        if i['username'] == username:
            if isAdmin(password, i['password']):
                return True
    return False

def generate_unique_id(db):
    while True:
        id = random.randrange(100000, 999999)
        for i in db:
            if i['project_id'] == id:
                continue
            else:
                return id
    

