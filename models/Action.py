import json
from sanic import Sanic
from metrograph import Action
from db.Connection import Connection
from redis.commands.json.path import Path

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
        return Connection.get_connection().json().get(f'action:{uuid}') != None

    def is_url_enabled(uuid) -> bool:
        if Action.exists(uuid):
            return Action.get(uuid).url_enabled
        return False

    def save(self) -> None:
        Connection.get_connection().json().set(f'action:{self.uuid}', Path.rootPath(), self.to_json())

    def get_all() -> list:
        actions = []
        for uuid in Connection.get_connection().scan_iter("action:*"):
            actions.append(Action.init_from_dict(Connection.get_connection().json().get(f'{uuid.decode()}')))
        return actions

    def init_from_dict(action: dict):
        return Action(uuid=action["uuid"], name=action["name"], description=action["description"], runtime=action["runtime"], runtime_version=action["runtime_version"], url_enabled=action["url_enabled"])

    def get(uuid: str):
        return Action.init_from_dict(Connection.get_connection().json().get(f'action:{uuid}'))

    def delete(self) -> None:
        Connection.get_connection().json().delete(f'action:{self.uuid}')

    def delete(uuid) -> None:
        Connection.get_connection().json().delete(f'action:{uuid}')

    def to_json(self) -> json:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "runtime": self.runtime,
            "runtime_version": self.runtime_version,
            "url_enabled": self.url_enabled
        }