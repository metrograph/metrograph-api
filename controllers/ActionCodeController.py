import uu
from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json
from models.ActionCode import ActionCode
from middleware.Auth import protected
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
