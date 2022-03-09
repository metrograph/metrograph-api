import json
from sanic import Sanic
from metrograph import task as MetroTask
from models.TaskConfig import TaskConfig
import pickle
import pickle

class Task:

    connection = Sanic.get_app().config.connection

    def __init__(
                    self, uuid: str, 
                    name:str, 
                    description: str,
                    config: TaskConfig) -> None:

        self.uuid = uuid
        self.name = name
        self.description = description
        self.config = config
        
        self.task = MetroTask(task_path = f"{config.compressed_package_path}/{self.uuid}.zip", python_version=config.runtime_version, flat_task_path=config.flat_package_path)
        self.task.unpack()
        self.task.prepare()

    def run(self) -> None:
        self.task.run()

    def __str__(self) -> str:
        return f'{self.uuid}'

    def save(self) -> None:
        Task.connection.set(f'task:{self.uuid}', pickle.dumps(self))

    def get_all() -> list:
        tasks = []
        for uuid in Task.connection.scan_iter("*"):
            tasks.append(Task.get(uuid.decode()))
        return tasks

    def get(uuid: str):
        task_bytes = Task.connection.get(uuid)
        object = pickle.loads(task_bytes)
        return object

    def __to_json__(self) -> json:
        return {
            "uuid": self.uuid,
            "task_name": self.name,
            "task_description": self.description,
            "config": self.config.__to_json__(),
        }