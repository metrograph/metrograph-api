from sanic import Sanic, Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, text, json
from middleware.Auth import protected
from models.Schedule import Schedule
from utils.RequestValidator import RequestValidator
from models.Action import Action
import uuid

app = Sanic.get_app()
schedule_bp = Blueprint('schedule', 'schedule', version=1)

@schedule_bp.route('/', methods=['GET'])
@protected
async def get_schedules(request: Request) -> HTTPResponse:
    return json({
                    "status" : "success",
                    "message" : "Schedules retrieved successfully",
                    "payload" : {
                        "schedules" : Schedule.get_all()
                    }
                })

@schedule_bp.route('/', methods=['POST'])
@protected
async def create_schedule(request: Request) -> HTTPResponse:
    
    if RequestValidator().validate(request=request, required_input=['action_uuid'], required_files=[]):
        
        action_uuid = request.json.get('action_uuid')
        weeks = request.json.get('weeks')
        days = request.json.get('days')
        hours = request.json.get('hours')
        minutes = request.json.get('minutes')
        seconds = request.json.get('seconds')
        at = request.json.get('at')
        times = request.json.get('times')
        enabled = request.json.get('enabled')

        if Action.exists(action_uuid):

            schedule = Schedule(uuid=str(uuid.uuid4()), action_uuid=action_uuid, \
                                weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds, at=at, times=times, enabled=enabled)
            schedule.save()
            
            await schedule.start(app)

            return json({
                "status" : "success",
                "message" : "Schedule created successfully",
                "payload" : {
                    "schedule" : schedule.__to_json__()
                }
            })
        else:
            return json({
                "status" : "error",
                "message" : "Action not found",
                "payload" : {
                    "uuid" : action_uuid
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
            "schedule_uid" : uuid
        }
    })

@schedule_bp.route('/<uuid>/enable', methods=['POST'])
@protected
async def enable_schedule(request:Request, uuid:str) -> HTTPResponse:
    return json({})

@schedule_bp.route('/<uuid>/disable', methods=['POST'])
@protected
async def disable_schedule(request:Request, uuid:str) -> HTTPResponse:
    return json({})