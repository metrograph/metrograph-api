import redis



class Connection:
    def __init__(self) -> None:
        self.connection = redis.Redis(
            host='redis-18213.c293.eu-central-1-1.ec2.cloud.redislabs.com',
            port=18213,
            db=0,
            password='2e5Ciyhe7p1TKgt95uP2emHQpybXIfiz'
        )
    
    def get_connection(self) -> redis.Redis:
        return self.connection;