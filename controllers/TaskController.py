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
    
    task = Task(uuid=task_uuid, config=task_config)
    task.save()
    

    





    #_t = MetroTask(task_path = f"{app.config.uploads_path}/{task_uid}.zip", python_version=language_version, flat_task_path=app.config.flat_tasks_path)
    #_t.unpack()
    #_t.prepare()
    #_t.run()

    return json({
        "status" : "success",
        "message" : "Task started successfully",
        "payload" : {
            "task_uid" : task.uuid
        }
    })

#TODO: To implement
@app.route("/task", methods=['DELETE'])
async def delete_task(request: Request) -> HTTPResponse:
    return json({
        "status" : "success",
        "message" : "Task deleted successfully",
        "payload" : {
            "task_uid" : ""
        }
    })

@app.route("/task/<uuid>/run", methods=['POST'])
async def run_task(request: Request, uuid) -> HTTPResponse:
    print("stating running:"+uuid)
    task = Task.get(uuid=uuid)
    task.run()
    return json({
        "status" : "success",
        "message" : "Task started successfully",
        "payload" : {
            "task_uid" : task.uuid
        }
    })
