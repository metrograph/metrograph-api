from sanic import Sanic
from cors.cors import add_cors_headers
from cors.options import setup_options
import db.Connection as Connection
from middleware.Auth import protected

class Server:

    #TODO: Get constants from a config file / env variables instead of hardcoding them

    def __init__(self) -> None:

        self.app = Sanic("metrograph-server", env_prefix='METRO_')
        self.app.config.update_config("${METRO_CONFIG_FILE}")

        self.app.config.compressed_packages_path = self.app.config.COMPRESSED_PACKAGES_PATH
        self.app.config.flat_packages_path = self.app.config.FLAT_PACKAGES_PATH
        self.app.config.guest_flat_packages_path = self.app.config.GUEST_FLAT_PACKAGES_PATH

    def setup_cors(self) -> None:
        self.app.register_listener(setup_options, "before_server_start")
        self.app.register_middleware(add_cors_headers, "response")

    def setup_db(self) -> None:
        self.app.config.connection = Connection.get_connection()


