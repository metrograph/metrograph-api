import json
from sanic import Sanic
from metrograph import task as MetroTask
from models.TaskConfig import TaskConfig
from db.Connection import Connection
import pickle

class Task:

    def __init__(
                    self, uuid: str, 
                    name:str, 
                    description: str,
                    config: TaskConfig,
                    url_enabled: bool = False) -> None:

        self.uuid = uuid
        self.name = name
        self.description = description
        self.config = config
        self.url_enabled = url_enabled
        
        self.task = MetroTask(task_path = f"{config.compressed_package_path}/{self.uuid}.zip", python_version=config.runtime_version, flat_task_path=config.flat_package_path)
        self.task.unpack()
        self.task.prepare()

    def __str__(self) -> str:
        return f'{self.uuid}'

    def exists(uuid) -> bool:
        return Connection.get_connection().get(f'task:{uuid}') != None

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