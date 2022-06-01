import redis

class Connection:

    connection =    connection = redis.Redis(
                        host='redis-18213.c293.eu-central-1-1.ec2.cloud.redislabs.com',
                        port=18213,
                        db=0,
                        password='5cpLGOIzKs6QhIy3D3C4ubUXCmQrkePe'
                    )

    def __init__(self) -> None:
        pass
    
    def get_connection() -> redis.Redis:
        return Connection.connection;