from uuid import uuid4
from models.User import User
from sanic import Request, Blueprint, HTTPResponse, json
from utils.RequestValidator import RequestValidator
import jwt

auth_bp = Blueprint('auth', url_prefix='auth', version=1)

@auth_bp.route("/register", methods=['POST'])
async def register(request: Request) -> HTTPResponse:
    
    validator = RequestValidator()
    if validator.validate(request=request, required_files=[], required_input=['username', 'password']):
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)
    
    if User.exists(username=request.json['username']):
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 409)

    user_uuid = str(uuid4())
    user = User(uuid=user_uuid, username=request.json['username'], password=request.json['password'])
    user.save()
    
    return json({
        "status" : "success",
        "message" : "User created successfully",
        "payload" : {
            "user" : user.__to_dict__()
        }
    })

@auth_bp.route("/", methods=['POST'])
async def authentificate(request: Request) -> HTTPResponse:

    validator = RequestValidator()
    if validator.validate(request=request, required_files=[], required_input=['username', 'password']):
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)
    
    if not User.exists(username=request.json['username']):
        print('incorrect username')
        return json({
            "status" : "error",
            "message" : "Unauthorized",
            "payload" : {}
        }, status = 401)
    
    user = User.get_by_username(username=request.json['username'])

    if not user.password == request.json['password']:
        print('incorrect passwor')
        return json({
            "status" : "error",
            "message" : "Unauthorized",
            "payload" : {}
        }, status = 401)
    
    user.update_token(jwt.encode({}, request.app.config.SECRET))

    return json({
        "status" : "success",
        "message" : "User authentificated successfully",
        "payload" : {
            "user" : user.__to_dict__()
        }
    })