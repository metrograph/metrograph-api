from sanic import Sanic
from db.Connection import Connection
from redis.commands.json.path import Path
import uuid

class User:

    def __init__(self, uuid:str, username:str, password:str, token:str = '') -> None:
        self.uuid=uuid
        self.username = username
        self.password = password
        self.token = token
    
    def init_from_dict(user:dict):
        if not user['token']:
            return User(uuid=user['uuid'], username=user['username'], password=user['password'])
        return User(uuid=user['uuid'], username=user['username'], password=user['password'], token=user['token'])

    def get_by_uuid(uuid: str):
        user = Connection.get_connection().json().get(f'user:{uuid}')
        return User.init_from_dict(user)
    
    def get_by_username(username: str):
        for u in Connection.get_connection().scan_iter("user:*"):
            user = Connection.get_connection().json().get(u.decode())
            if user['username'] == username:
                return User.init_from_dict(user)
        return None

    def exists(username: str) -> bool:
        for u in Connection.get_connection().scan_iter("user:*"):
            user = Connection.get_connection().json().get(u.decode())
            if user['username'] == username:
                return True
        return False 

    def authentificate(username: str, password: str):
        for u in Connection.get_connection().scan_iter("user:*"):
            user = Connection.get_connection().json().get(u.decode())
            if user['username'] == username and user['password'] == password:
                return user
        return None 

    def __repr__(self):
        return "User(uuid='{}')".format(self.uuid)

    def __to_dict__(self):
        return {"uuid": self.uuid, "username": self.username, "token": self.token}

    def save(self):
        Connection.get_connection().json().set(f'user:{self.uuid}', Path.rootPath(), 
        {"uuid": self.uuid, "username": self.username, "password": self.password, "token": self.token})

    def update_token(self, token:str):
        self.token = token
        self.save()