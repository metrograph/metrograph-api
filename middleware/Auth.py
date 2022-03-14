from models.User import User
from sanic import Request
import jwt

class Auth:

    def authentificate(request: Request) -> bool:
        if not request.token:
            return False
        try:
            user_req = jwt.decode(request.token, request.app.config.SECRET, algorithms=["HS256"])
            user_db = User.get_by_username(username=user_req.username)
            if not user_db:
                return False
            if not user_db.token == user_req.token:
                return False
        except jwt.exceptions.InvalidTokenError:
            return False
        return True



