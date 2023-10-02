import json
import bcrypt

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


