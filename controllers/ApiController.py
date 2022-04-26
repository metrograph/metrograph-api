from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, text, json

api_bp = Blueprint('api', url_prefix='api', version=1)

@api_bp.route('/<uuid>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
async def call_action(request: Request, uuid:str):
    return json({
        "message": "success"
    })