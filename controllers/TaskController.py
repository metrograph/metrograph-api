from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, text, json
from metrograph import task as MetroTask
import os
import uuid
import aiofiles


app = Sanic.get_app()

@app.route("/", methods=['GET'])
async def index(request: Request) -> HTTPResponse:
    return json({
        "status" : "success",
        "message" : "hello"
    })

@app.route("/task", methods=['POST'])
async def index(request: Request) -> HTTPResponse:
    task_package = request.files.get("task_package")
    print(type(task_package))
    
    
    language = request.form.get("language")
    language_version = request.form.get("version")

    if not os.path.exists(app.config.uploads_path):
        os.makedirs(app.config.uploads_path)

    task_uid = str(uuid.uuid4())
    
    async with aiofiles.open(f"{app.config.uploads_path}/{task_uid}.zip", 'wb') as f:
        await f.write(request.files["task_package"][0].body)
    f.close()

    _t = MetroTask(task_path = f"{app.config.uploads_path}/{task_uid}.zip", python_version=language_version, flat_task_path=app.config.flat_tasks_path)
    _t.unpack()
    _t.prepare()
    _t.run()

    return json({
        "status" : "success",
        "message" : "Task started successfully",
        "task_id" : _t.task_uid
    })
