from uuid import uuid4
from models.User import User
from sanic import Request, Blueprint, HTTPResponse, json
from utils.RequestValidator import RequestValidator
import jwt
from datetime import datetime
import bcrypt
from middleware.Auth import protected

auth_bp = Blueprint('auth', url_prefix='auth', version=1)

@auth_bp.route("/register", methods=['POST'])
async def register(request: Request) -> HTTPResponse:
    
    validator = RequestValidator()
    if not validator.validate(request=request, required_files=[], required_input=['username', 'password']):
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)
    
    if User.exists(username=request.json['username']):
        return json({
            "status" : "error",
            "message" : "Conflict",
            "payload" : {}
        }, status = 409)

    user_uuid = str(uuid4())
    hashed_pw = bcrypt.hashpw(str.encode(request.json['password']), bcrypt.gensalt())
    user = User(uuid=user_uuid, username=request.json['username'], password=hashed_pw.decode())
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
    if not validator.validate(request=request, required_files=[], required_input=['username', 'password']):
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)
    
    if not User.exists(username=request.json['username']):
        return json({
            "status" : "error",
            "message" : "Unauthorized",
            "payload" : {}
        }, status = 401)
    
    user = User.get_by_username(username=request.json['username'])

    if not bcrypt.checkpw(str.encode(request.json['password']), str.encode(user.password)):
        return json({
            "status" : "error",
            "message" : "Unauthorized",
            "payload" : {}
        }, status = 401)
    
    user.update_token(jwt.encode({  "user": {"username" : user.username}, 
                                    "time": str(datetime.today().timestamp())
                                    }, request.app.config.SECRET))

    return json({
        "status" : "success",
        "message" : "User authentificated successfully",
        "payload" : {
            "user" : user.__to_dict__()
        }
    })