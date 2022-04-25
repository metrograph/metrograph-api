from sanic import Sanic, text
from utils import Server

server = Server.Server()
server.setup_cors()
server.setup_db()
server.resume_schedules()


app = Sanic.get_app()
app.config.SECRET = "KEEP_IT_SECRET_KEEP_IT_SAFE"

from controllers.AuthController import auth_bp
from controllers.TaskController import task_bp
from controllers.ScheduleController import schedule_bp

app.blueprint(auth_bp)
app.blueprint(task_bp)
app.blueprint(schedule_bp)

app.run(host='0.0.0.0', port=1337, access_log=False, fast=True, auto_reload=True)