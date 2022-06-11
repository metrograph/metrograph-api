from functools import wraps
from models.User import User
from sanic import Request, json
import jwt
import redis

def is_authentificated(request: Request) -> bool:
    if not request.token:
        return False
    try:
        decoded = jwt.decode(request.token, request.app.config.SECRET, algorithms=["HS256"])
        user_token = decoded['user']
        time_token = decoded['time']
        user_db = User.get_by_username(username=user_token['username'])
        if not user_db:
            return False
        if user_db.token != request.token:
            return False
    except jwt.exceptions.InvalidTokenError:
        return False
    request.ctx.token = request.token
    request.ctx.user = user_db
    return True

def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            
            if is_authentificated(request=request):
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json({
                    "status" : "error",
                    "message" : "Unauthorized",
                    "payload" : {}
                }, status = 401)
        return decorated_function
    return decorator(wrapped)

