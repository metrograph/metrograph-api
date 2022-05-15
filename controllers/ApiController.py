from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, text, json
from models.Task import Task
import boto3
from botocore.client import Config
from models.ActionCode import ActionCode
from models.Files import Folder

api_bp = Blueprint('api', url_prefix='api', version=1)

@api_bp.route('/<uuid>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
async def call_action(request: Request, uuid: str):
    tree = ActionCode.create_new("123", "python", "3.9.10")
    Folder.print_tree(tree)
    return json({
        "message": "success"
    })
    