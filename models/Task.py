from os import path
import sys
from sanic import Sanic
from db import Connection
from metrograph import task as MetroTask
from models.TaskConfig import TaskConfig
import pickle
from db.Connection import Connection

class Task:

    connection = Sanic.get_app().config.connection

    def __init__(self, uuid: str, config: TaskConfig) -> None:

        self.uuid = uuid
        self.config = config
        self.task = MetroTask(task_path = f"{config.compressed_package_path}/{self.uuid}.zip", python_version=config.runtime_version, flat_task_path=config.flat_package_path)
        
        self.task.unpack()
        self.task.prepare()

    def run(self) -> None:
        self.task.run()

    def __str__(self) -> str:
        return f'{self.uuid}'

    def save(self) -> None:
        Task.connection.set(self.uuid, pickle.dumps(self))

    def get(uuid: str):
        print(uuid)
        task_bytes = Task.connection.get(uuid)
        print("RESULT #########")
        print(task_bytes)
        object = pickle.loads(task_bytes)
        return object

