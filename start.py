from sanic import Sanic, text
from utils import Server

server = Server.Server()
server.setup_cors()
server.setup_db()
#server.setup_scheduler()

app = Sanic.get_app()
app.config.SECRET = "KEEP_IT_SECRET_KEEP_IT_SAFE"

from controllers.AuthController import auth_bp
from controllers.ActionController import action_bp
from controllers.ActionCodeController import actioncode_bp
#from controllers.ScheduleController import schedule_bp
#from controllers.ApiController import api_bp

app.blueprint(auth_bp)
app.blueprint(action_bp)
app.blueprint(actioncode_bp)
#app.blueprint(schedule_bp)
#app.blueprint(api_bp)

app.run(host='0.0.0.0', port=1337, access_log=False, fast=True, auto_reload=True)