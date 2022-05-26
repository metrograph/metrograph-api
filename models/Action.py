import json
from sanic import Sanic
from metrograph import Action
from db.Connection import Connection
import pickle

class Action:

    def __init__(   self, 
                    uuid: str, 
                    name:str, 
                    description: str,
                    runtime: str,
                    runtime_version: str,
                    url_enabled: bool = False) -> None:

        self.uuid = uuid
        self.name = name
        self.description = description
        self.runtime = runtime
        self.runtime_version = runtime_version
        self.url_enabled = url_enabled

    def exists(uuid) -> bool:
        return Connection.get_connection().get(f'action:{uuid}') != None

    def is_url_enabled(uuid) -> bool:
        if Action.exists(uuid):
            return Action.get(uuid).url_enabled
        return False

    def run(self) -> None:
        self.task.run()

    def save(self) -> None:
        Connection.get_connection().set(f'task:{self.uuid}', pickle.dumps(self))

    def get_all() -> list:
        tasks = []
        for uuid in Connection.get_connection().scan_iter("task:*"):
            tasks.append(pickle.loads(Connection.get_connection().get(f'{uuid.decode()}')))
        return tasks

    def get(uuid: str):
        return pickle.loads(Connection.get_connection().get(f'task:{uuid}'))

    def delete(self) -> None:
        Connection.get_connection().delete(f'task:{self.uuid}')

    def delete(uuid) -> None:
        Connection.get_connection().delete(f'task:{uuid}')

    def __to_json__(self) -> json:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "url_enabled": self.url_enabled,
            "config": self.config.__to_json__()
        }