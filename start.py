from sanic import Sanic
from utils import Server

server = Server.Server()
server.setup_cors()

import controllers.TaskController

app = Sanic.get_app()
app.run(host='0.0.0.0', port=1337, access_log=False, fast=True)