from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from sanic import Sanic
from cors.cors import add_cors_headers
from cors.options import setup_options

class Server:

    #TODO: Get constants from a config file / env variables instead of hardcoding them

    def __init__(self) -> None:

        self.app = Sanic("metrograph-server", env_prefix='METRO_')
        self.app.config.uploads_path = "/home/metrograph/uploads"
        self.app.config.flat_tasks_path = "/home/metrograph/flat_tasks/"
        self.app.config.guest_flat_task_path = '/usr/src/app'

    def setup_cors(self) -> None:
        # Add OPTIONS handlers to any route that is missing it
        self.app.register_listener(setup_options, "before_server_start")
        # Fill in CORS headers
        self.app.register_middleware(add_cors_headers, "response")