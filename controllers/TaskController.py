from sanic import Sanic
from sanic.request import Request, File
from sanic.response import HTTPResponse, text, json
from metrograph import task as MetroTask
import os
import uuid
import aiofiles
from models.Task import Task
from models.TaskConfig import TaskConfig
from utils.RequestValidator import RequestValidator

from utils.ResponseEncoder import ResponseEncoder

app = Sanic.get_app()

@app.route("/", methods=['GET'])
async def index(request: Request) -> HTTPResponse:
    return json({
        "status" : "success",
        "message" : "API version: 0.0.1"
    })

@app.route("/task", methods=['GET'])
async def get_tasks(request: Request) -> HTTPResponse:
    return json({
        "status" : "success",
        "message" : "Tasks retreived successfully",
        "payload" : {
            "tasks" : [t.__to_json__() for t in Task.get_all()]
        }
    })

@app.route("/task/<uuid>", methods=['GET'])
async def get_tasks(request: Request, uuid) -> HTTPResponse:
    return json({
        "status" : "success",
        "message" : "Task retreived successfully",
        "payload" : {
            "task" : Task.get(uuid).__to_json__()
        }
    })

#TODO: Validate input + manage exceptions
@app.route("/task", methods=['POST'])
async def create_task(request: Request) -> HTTPResponse:

    print(type(request.files.get("task_package")))

    validator = RequestValidator()
    if not validator.validate(required_files=['task_package'],required_input=['task_name', 'runtime', 'runtime_version'], request=request):
        print('validation failed')
        return json({
            "status" : "error",
            "message" : "Invalid request",
            "payload" : {}},
            status=400
        )
    else:
        print('validation successful')

    task_config = TaskConfig(
                    compressed_package_path=app.config.compressed_packages_path, 
                    flat_package_path=app.config.flat_packages_path,
                    runtime=request.form.get('runtime'),
                    runtime_version=request.form.get('runtime_version'))
    
    if not os.path.exists(app.config.compressed_packages_path):
        os.makedirs(app.config.compressed_packages_path)
    
    task_uuid = str(uuid.uuid4())

    async with aiofiles.open(f"{app.config.compressed_packages_path}/{task_uuid}.zip", 'wb') as f:
        await f.write(request.files["task_package"][0].body)
    f.close()
    
    task = Task(uuid=task_uuid, name=request.form.get("task_name"), description=request.form.get("task_description"), config=task_config)
    task.save()

    return json({
        "status" : "success",
        "message" : "Task started successfully",
        "payload" : {
            "task" : task.__to_json__()
        }
    })

@app.route("/task/<uuid>", methods=['DELETE'])
async def run_task(request: Request, uuid) -> HTTPResponse:
    Task.delete(uuid=uuid)
    return json({
        "status" : "success",
        "message" : "Task deleted successfully",
        "payload" : {
            "task_uid" : uuid
        }
    })

@app.route("/task/<uuid>/run", methods=['POST'])
async def run_task(request: Request, uuid) -> HTTPResponse:
    task = Task.get(uuid=f'{uuid}')
    task.run()
    return json({
        "status" : "success",
        "message" : "Task started successfully",
        "payload" : {
            "task_uid" : task.uuid
        }
    })


