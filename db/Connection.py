from sanic import Sanic
import redis

class Connection:

    connection =    redis.Redis(
                        host=       Sanic.get_app().config.DB_HOSTNAME,
                        port=       Sanic.get_app().config.DB_PORT,
                        db=         Sanic.get_app().config.DB_DBN,
                        password=   Sanic.get_app().config.DB_PASSWORD
                    )

    def __init__(self) -> None:
        pass
    
    def get_connection() -> redis.Redis:
        return Connection.connection;