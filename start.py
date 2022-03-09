from sanic import Sanic
from utils import Server
import db.Connection as Connection

server = Server.Server()
server.setup_cors()

app = Sanic.get_app()
app.config.connection = Connection().get_connection()


from controllers import TaskController


app.run(host='0.0.0.0', port=1337, access_log=False, fast=True, auto_reload=True)