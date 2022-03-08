from os import path
import sys
from sanic import Sanic
import uuid
from db import Connection
from metrograph import task as MetroTask
from models.TaskConfig import TaskConfig

class Task:

    def __init__(self, config: TaskConfig) -> None:

        self.uuid = str(uuid.uuid4())
        self.config = config
        self.task = MetroTask(task_path = f"{config.flat_package_path}/{self.uuid}.zip", python_version=config.runtime_version, flat_task_path=config.flat_package_path)
    
    def unpack(self) -> None:
        try:
            self.task.unpack()
        except Exception:
            print('An error has accured while unpacking the Task')
            pass

    def prepare(self) -> None:
        pass