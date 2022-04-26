from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, text, json
from middleware.Auth import protected
from models.Schedule import Schedule
from utils.RequestValidator import RequestValidator
from models.Task import Task
import uuid


app = Sanic.get_app()
schedule_bp = Blueprint('schedule', 'schedule', version=1)

@schedule_bp.route('/', methods=['GET'])
@protected
async def get_schedules(request: Request) -> HTTPResponse:
    return json({
        "message": Schedule.get_all()
    })

@schedule_bp.route('/', methods=['POST'])
@protected
async def create_schedule(request: Request) -> HTTPResponse:
    
    if RequestValidator().validate(request=request, required_input=['task_uuid'], required_files=[]):
        
        task_uuid = request.json.get('task_uuid')
        weeks = request.json.get('weeks')
        days = request.json.get('days')
        hours = request.json.get('hours')
        minutes = request.json.get('minutes')
        seconds = request.json.get('seconds')
        at = request.json.get('at')
        times = request.json.get('times')

        if Task.exists(task_uuid):

            schedule = Schedule(uuid=str(uuid.uuid4()), task_uuid=task_uuid, \
                                weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds, at=at, times=times)
            if schedule.start():
                schedule.save()

                return json({
                    "status" : "success",
                    "message" : "Schedule created successfully",
                    "payload" : {
                        "task" : schedule.__to_json__()
                    }
                })
        else:
            return json({
                "status" : "error",
                "message" : "Task not found",
                "payload" : {
                    "uuid" : task_uuid
                }
            }, status = 404)

    return json({
        "status" : "error",
        "message" : "Bad request",
        "payload" : {}},
        status=400
    )

@schedule_bp.route('/<uuid>', methods=['DELETE'])
@protected
async def delete_schedule(request:Request, uuid:str) -> HTTPResponse:
    if uuid == '':
        return json({
            "status" : "error",
            "message" : "Bad request",
            "payload" : {}
        }, status = 400)

    if not Schedule.exists(uuid):
        return json({
            "status" : "error",
            "message" : "Schedule not found",
            "payload" : {
                "uuid" : uuid
            }
        }, status = 404)
    
    Schedule.delete(uuid=uuid)
    return json({
        "status" : "success",
        "message" : "Schedule deleted successfully",
        "payload" : {
            "task_uid" : uuid
        }
    })