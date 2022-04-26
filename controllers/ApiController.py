from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, text, json
from models.Task import Task

api_bp = Blueprint('api', url_prefix='api', version=1)

@api_bp.route('/<uuid>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
async def call_action(request: Request, uuid:str):
    if Task.is_url_enabled(uuid):\
        return json({
            "message": "success"
        })
    else:
        return json({
            "message": "not found"
        }, status=404)