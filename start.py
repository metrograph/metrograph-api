
# Instanciating the app and adding it to registry
from sanic import Sanic
app = Sanic("metrograph-server", env_prefix='METROGRAPH_')

# Global App Configuration
from utils import Server
server = Server.Server()
server.setup_cors()
server.setup_db()
server.setup_encryption()
server.setup_scheduler()

# Controllers Config

from controllers.AuthController import auth_bp
from controllers.ActionController import action_bp
from controllers.ActionCodeController import actioncode_bp
from controllers.ScheduleController import schedule_bp
#from controllers.ApiController import api_bp

app.blueprint(auth_bp)
app.blueprint(action_bp)
app.blueprint(actioncode_bp)
app.blueprint(schedule_bp)
#app.blueprint(api_bp)

# Starting App
app.run(host='0.0.0.0', port=1337, access_log=True, fast=True, auto_reload=True)