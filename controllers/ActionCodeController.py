import uu
from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json, file, file_stream
from models.ActionCode import ActionCode
from middleware.Auth import protected
from pathlib import Path
import uuid

from models.Files.Folder import Folder

app = Sanic.get_app()
actioncode_bp = Blueprint('actioncode', url_prefix='actioncode', version=1)

@actioncode_bp.route("/<uuid>", methods=['GET'])
@protected
async def get_actioncode(request: Request, uuid) -> HTTPResponse:

    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not ActionCode.exists(uuid):
        return json({
            "status" : "error",
            "message" : "ActionCode not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)

    return json({
        "status" : "success",
        "message" : "Action retreived successfully",
        "payload" : {
            "ActionCode" : ActionCode.get_by_uuid(uuid=uuid).get_json_tree()
        }
    })

@actioncode_bp.route("/<uuid>/file", methods=['GET'])
@protected
async def get_file_content(request: Request, uuid) -> HTTPResponse:
    
    if uuid == '' or not request.json.get('path'):
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    file_path = ActionCode.ACTIONS_PATH + request.json.get('path')

    if not ActionCode.exists(uuid) or not Path(file_path).exists() or not Path(file_path).is_file():
        return json({
            "status" : "error",
            "message" : "ActionCode not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)

    if Path(file_path).exists() and Path(file_path).is_file():
        return await file(file_path)
    else:
        return json({
            "status" : "error",
            "message" : "File not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)


@actioncode_bp.route("/<uuid>/folder", methods=['POST'])
@protected
async def create_folder(request: Request, uuid) -> HTTPResponse:
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not ActionCode.exists(uuid):
        return json({
            "status" : "error",
            "message" : "ActionCode not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    ActionCode.create_folder(request.json.get('path'))
    
    return json({
        "status" : "success",
        "message" : "Folder created succesfully",
        "payload" : {
            "uuid" : uuid
        }
    })

@actioncode_bp.route("/<uuid>/file", methods=['POST'])
@protected
async def create_file(request: Request, uuid) -> HTTPResponse:
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not ActionCode.exists(uuid):
        return json({
            "status" : "error",
            "message" : "ActionCode not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    ActionCode.create_file(request.json.get('path'))
    
    return json({
        "status" : "success",
        "message" : "File created succesfully",
        "payload" : {
            "uuid" : uuid
        }
    })

@actioncode_bp.route("/<uuid>/folder", methods=['PATCH'])
@protected
async def rename_folder(request: Request, uuid) -> HTTPResponse:
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not ActionCode.exists(uuid):
        return json({
            "status" : "error",
            "message" : "ActionCode not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    ActionCode.rename_folder(request.json.get('path'), request.json.get('new_name'))
    
    return json({
        "status" : "success",
        "message" : "Folder renamed succesfully",
        "payload" : {
            "uuid" : uuid
        }
    })

@actioncode_bp.route("/<uuid>/file", methods=['PATCH'])
@protected
async def rename_file(request: Request, uuid) -> HTTPResponse:
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not ActionCode.exists(uuid):
        return json({
            "status" : "error",
            "message" : "ActionCode not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    ActionCode.rename_file(request.json.get('path'), request.json.get('new_name'))
    
    return json({
        "status" : "success",
        "message" : "File renamed succesfully",
        "payload" : {
            "uuid" : uuid
        }
    })

@actioncode_bp.route("/<uuid>/file", methods=['DELETE'])
@protected
async def delete_file(request: Request, uuid) -> HTTPResponse:
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not ActionCode.exists(uuid):
        return json({
            "status" : "error",
            "message" : "ActionCode not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    ActionCode.delete_file(request.json.get('path'))
    
    return json({
        "status" : "success",
        "message" : "File deleted succesfully",
        "payload" : {
            "uuid" : uuid
        }
    })

@actioncode_bp.route("/<uuid>/folder", methods=['DELETE'])
@protected
async def delete_folder(request: Request, uuid) -> HTTPResponse:
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not ActionCode.exists(uuid):
        return json({
            "status" : "error",
            "message" : "ActionCode not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    ActionCode.delete_folder(request.json.get('path'))
    
    return json({
        "status" : "success",
        "message" : "Folder deleted succesfully",
        "payload" : {
            "uuid" : uuid
        }
    })

@actioncode_bp.route("/<uuid>/file", methods=['PUT'])
@protected
async def update_file(request: Request, uuid) -> HTTPResponse:
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not ActionCode.exists(uuid):
        return json({
            "status" : "error",
            "message" : "ActionCode not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    if ActionCode.update_file(request.json.get('path'), request.json.get('content')):
        return json({"msg":"ok"})
    else:
        return json({"msg":"not found"})

