from sanic import Sanic
from cors.cors import add_cors_headers
from cors.options import setup_options
import db.Connection as Connection
from scheduler.Scheduler import start_background_scheduler, stop_background_scheduler

class Server:

    def __init__(self) -> None:
        self.app = Sanic.get_app()
        
    def setup_cors(self) -> None:
        self.app.register_listener(setup_options, "before_server_start")
        self.app.register_middleware(add_cors_headers, "response")

    def setup_db(self) -> None:
        self.app.config.connection = Connection.get_connection()

    def setup_encryption(self) -> None:
        self.app.config.SECRET = self.app.config.ENCRYPTION_KEY

    def setup_scheduler(self) -> None:
        self.app.register_listener(start_background_scheduler, "main_process_start")
        self.app.register_listener(stop_background_scheduler, "main_process_stop")
