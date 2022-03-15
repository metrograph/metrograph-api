from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, text, json
import os
import uuid
import aiofiles
from models.Task import Task
from models.TaskConfig import TaskConfig
from utils.RequestValidator import RequestValidator
from utils.ResponseEncoder import ResponseEncoder
from middleware.Auth import protected

app = Sanic.get_app()
task_bp = Blueprint('task', url_prefix='task', version=1)

@task_bp.route("/", methods=['GET'])
@protected
async def get_tasks(request: Request) -> HTTPResponse:
    return json({
        "status" : "success",
        "message" : "Tasks retreived successfully",
        "payload" : {
            "tasks" : [t.__to_json__() for t in Task.get_all()]
        }
    })

@task_bp.route("/<uuid>", methods=['GET'])
@protected
async def get_task(request: Request, uuid) -> HTTPResponse:

    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not Task.exists(uuid):
        return json({
            "status" : "error",
            "message" : "Task not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)

    return json({
        "status" : "success",
        "message" : "Task retreived successfully",
        "payload" : {
            "task" : Task.get(uuid).__to_json__()
        }
    })

@task_bp.route("/", methods=['POST'])
@protected
async def create_task(request: Request) -> HTTPResponse:

    if not RequestValidator().validate(required_files=['task_package'],required_input=['task_name', 'runtime', 'runtime_version'], request=request):
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}},
            status=400
        )
    
    if not request.files["task_package"][0].name.endswith('.zip'):
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}},
            status=400
        )

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
        "message" : "Task created successfully",
        "payload" : {
            "task" : task.__to_json__()
        }
    })

@task_bp.route("/<uuid>", methods=['DELETE'])
@protected
async def delete_task(request: Request, uuid) -> HTTPResponse:
    
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not Task.exists(uuid):
        return json({
            "status" : "error",
            "message" : "Task not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    Task.delete(uuid=uuid)
    return json({
        "status" : "success",
        "message" : "Task deleted successfully",
        "payload" : {
            "task_uid" : uuid
        }
    })

@task_bp.route("/<uuid>/run", methods=['POST'])
@protected
async def run_task(request: Request, uuid) -> HTTPResponse:
    
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not Task.exists(uuid):
        return json({
            "status" : "error",
            "message" : "Task not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    task = Task.get(uuid=f'{uuid}')
    task.run()
    return json({
        "status" : "success",
        "message" : "Task started successfully",
        "payload" : {
            "task_uid" : task.uuid
        }
    })


