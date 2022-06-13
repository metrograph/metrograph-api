from db.Connection import Connection
from sanic.response import json
from redis.commands.json.path import Path

class Schedule:

    def __init__(self, uuid: str, action_uuid: str, weeks=None, days=None, hours=None, minutes=None, seconds=None, at=None, times=None, num_executions=0, enabled=True, loaded=False):
        self.uuid = uuid
        self.action_uuid = action_uuid
        self.weeks = weeks
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.at = at
        self.times = -1
        if times:
            self.times = times
        self.num_executions = num_executions
        self.enabled = enabled
        self.loaded = loaded

    def get_all() -> list:
        schedules = []
        for uuid in Connection.get_connection().scan_iter('schedule:*'):
            schedules.append(Connection.get_connection().json().get(f'{uuid.decode()}'))
        return schedules

    def get_by_uuid(uuid) -> bool:
        return Schedule.init_from_dict(Connection.get_connection().json().get(f'schedule:{uuid}'))

    def init_from_dict(sc: dict):
        schedule = Schedule(sc["uuid"], sc["action_uuid"], sc["weeks"], sc["days"], sc["hours"], sc["minutes"], sc["seconds"], sc["at"], sc["times"], sc["num_executions"], sc["enabled"], sc["loaded"])
        return schedule

    def exists(uuid) -> bool:
        return Connection.get_connection().json().get(f'schedule:{uuid}') != None

    def save(self) -> None:
        Connection.get_connection().json().set(f'schedule:{self.uuid}', Path.rootPath(), self.__to_json__())

    def delete(uuid: str) -> None:
        Connection.get_connection().json().delete(f'schedule:{uuid}')

    def increment_executions(self):
        self.num_executions += 1
        Connection.get_connection().json().set(f'schedule:{self.uuid}', Path.rootPath(), self.__to_json__())

    def __to_json__(self) -> json:
        return {
            "uuid": self.uuid,
            "action_uuid": self.action_uuid,
            "weeks": self.weeks,
            "days": self.days,
            "hours": self.hours,
            "minutes": self.minutes,
            "seconds": self.seconds,
            "at": self.at,
            "times": self.times,
            "num_executions": self.num_executions,
            "enabled": self.enabled,
            "loaded": self.loaded
        }