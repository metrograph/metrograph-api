from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json
from models.Action import Action
from models.ActionCode import ActionCode
from utils.RequestValidator import RequestValidator
from middleware.Auth import protected
import metrograph
import uuid

app = Sanic.get_app()
action_bp = Blueprint('action', url_prefix='action', version=1)

@action_bp.route("/", methods=['GET'])
@protected
async def get_actions(request: Request) -> HTTPResponse:
    try:
        return json({
            "status" : "success",
            "message" : "Actions retreived successfully",
            "payload" : {
                "actions" : [a.to_json() for a in Action.get_all()]
            }
        })
    except Exception as e:
        return json({
                "status" : "error",
                "message" : "Failed to retreive actions",
                "payload" : {
                    "error_type" : "database_error",
                    "error_message": f'{e}'
                }
            }, status=500)

@action_bp.route("/<uuid>", methods=['GET'])
@protected
async def get_action(request: Request, uuid:str) -> HTTPResponse:
    
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not Action.exists(uuid):
        return json({
            "status" : "error",
            "message" : "Action not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)

    try:
        return json({
            "status" : "success",
            "message" : "Action retreived successfully",
            "payload" : {
                "ActionCode" : Action.get(uuid=uuid).to_json()
            }
        })
    except Exception as e:
        return json({
                "status" : "error",
                "message" : "Failed to retreive action",
                "payload" : {
                    "error_type" : "database_error",
                    "error_message": f'{e}'
                }
            }, status=500)

@action_bp.route("/", methods=['POST'])
@protected
async def create_action(request: Request) -> HTTPResponse:
    if not RequestValidator().validate(required_files=[], required_input=['name', 'description', 'runtime', 'runtime_version'], request=request):
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}},
            status=400
        )

    action_uuid = str(uuid.uuid4())
    name = request.json.get('name')
    description = request.json.get('description')
    runtime = request.json.get('runtime')
    runtime_version = request.json.get('runtime_version')
    url_enabled = False

    if request.json.get('url_enabled'):
        url_enabled = request.json.get('url_enabled')

    action = Action(uuid=action_uuid, name=name, description=description, runtime=runtime, runtime_version=runtime_version, url_enabled=url_enabled)
    ActionCode.create_new(uuid=action.uuid, runtime=action.runtime, runtime_version=action.runtime_version)
    
    try:
        action.build_image()
        action.save()
        return json({
                    "status" : "success",
                    "message" : "Action created successfully",
                    "payload" : {
                        "action" : action.to_json()
                    }
                })
    except Exception as e:
        return json({
                    "status" : "error",
                    "message" : "Action creation error",
                    "payload" : {
                        "error_type" : "action_error",
                        "error_message": f'{e}'
                    }
                }, status = 500)


@action_bp.route("/<uuid>", methods=['PATCH'])
@protected
async def edit_action(request: Request, uuid:str) -> HTTPResponse:

    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not Action.exists(uuid):
        return json({
            "status" : "error",
            "message" : "Action not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    action = Action.get(uuid=uuid)

    if request.json.get('name'):
        action.name = request.json.get('name')

    if request.json.get('description'):
        action.description = request.json.get('description')

    if request.json.get('runtime'):
        action.runtime = request.json.get('runtime')

    if request.json.get('runtime_version'):
        action.runtime_version = request.json.get('runtime_version')

    if request.json.get('url_enabled'):
        action.url_enabled = request.json.get('url_enabled')

    action.save()

    return json({
                "status" : "success",
                "message" : "Action updated successfully",
                "payload" : {
                    "action" : action.to_json()
                }
            })

@action_bp.route("/<uuid>", methods=['DELETE'], ignore_body=False)
@protected
async def delete_action(request: Request, uuid) -> HTTPResponse:
    
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not Action.exists(uuid):
        return json({
            "status" : "error",
            "message" : "Action not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    Action.delete(uuid=uuid)
    ActionCode.delete(uuid=uuid)

    return json({
        "status" : "success",
        "message" : "Action deleted successfully",
        "payload" : {
            "action_uid" : uuid
        }
    })

@action_bp.route("/<uuid>/image/build", methods=['POST'])
@protected
async def build_action_image(request: Request, uuid) -> HTTPResponse:
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not Action.exists(uuid):
        return json({
            "status" : "error",
            "message" : "Action not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)

    Action.get(uuid).build_image()

    return json({
        "status" : "success",
        "message" : "Action image built successfully",
        "payload" : {
            "action_uid" : uuid
        }
    })

@action_bp.route("/<uuid>/run", methods=['POST'])
@protected
async def run_action(request: Request, uuid) -> HTTPResponse:
    
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not Action.exists(uuid):
        return json({
            "status" : "error",
            "message" : "Action not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    try:

        action = Action.get(uuid=f'{uuid}')
        action.run()

        return json({
            "status" : "success",
            "message" : "Action started successfully",
            "payload" : {
                "action_uid" : action.uuid
            }
        })

    except metrograph.errors.ImageNotFound as e:
        return json({
                "status" : "error",
                "message" : "Failed to run the action",
                "payload" : {
                    "action_uuid": action.uuid,
                    "error_type" : "image_not_found",
                    "error_message": f'{e}'
                }
            }, status=500)

    except metrograph.errors.APIError as e:
        return json({
                "status" : "error",
                "message" : "Failed to run the action",
                "payload" : {
                    "action_uuid": action.uuid,
                    "error_type" : "api_error",
                    "error_message": f'{e}'
                }
            }, status=500)

    except metrograph.errors.ContainerError as e:
        return json({
                "status" : "error",
                "message" : "Failed to run the action",
                "payload" : {
                    "action_uuid": action.uuid,
                    "error_type" : "container_error",
                    "error_message": f'{e}'
                }
            }, status=500)

    except Exception as e:
        return json({
                "status" : "error",
                "message" : "Failed to run the action",
                "payload" : {
                    "action_uuid": action.uuid,
                    "error_type" : "other_error",
                    "error_message": f'{e}'
                }
            }, status=500)
    
    

