from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, text
from metrograph import task as MetroTask
import os
import uuid
import aiofiles

app = Sanic("metrograph-api")

app.config.uploads_path = "/home/hamza/Projects/Jupyter/metrograpgh/uploads/"
app.config.flat_tasks_path = "/home/hamza/Projects/Jupyter/metrograpgh/flat_tasks/"
app.config.guest_flat_task_path = '/usr/src/app'

@app.post("/task")
async def index(request: Request) -> HTTPResponse:
    task_package = request.files.get("task_package")
    print(type(task_package))
    
    
    language = request.form.get("language")
    language_version = request.form.get("version")

    if not os.path.exists(app.config.uploads_path):
        os.makedirs(app.config.uploads_path)

    task_file_name = str(uuid.uuid4())
    
    async with aiofiles.open(f"{app.config.uploads_path}/{task_file_name}.zip", 'wb') as f:
        await f.write(request.files["task_package"][0].body)
    f.close()

    _t = MetroTask(task_path = f"{app.config.uploads_path}/{task_file_name}.zip", python_version=language_version, flat_task_path=app.config.flat_tasks_path)
    print(_t)
    _t.unpack()
    _t.prepare()
    _t.run()

    return text("Task completed successfully!")

