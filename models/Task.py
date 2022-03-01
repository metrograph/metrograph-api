from os import path
import sys
from sanic import Sanic
import uuid
from db import Connection
from metrograph import task as MetroTask

class Task:

    def __init__(self, 
                    compressed_package_path : str = None,
                    runtime : str = None,
                    runtime_version: str = None
    ) -> None:

        self.uuid = str(uuid.uuid4())
        self.task = MetroTask(task_path = f"{self.app.config.uploads_path}/{self.uuid}.zip", python_version=runtime_version, flat_task_path=self.app.config.flat_tasks_path)
    
    def unpack(self) -> None:
        try:
            self.task.unpack()
        except Exception:
            print('An error has accured while unpacking the Task')
            pass

    def prepare(self) -> None:
        pass