from db.Connection import Connection
from sanic.response import json
from redis.commands.json.path import Path
from scheduler.Scheduler import schedule_task

class Schedule:

    def __init__(self, uuid: str, task_uuid: str, weeks=None, days=None, hours=None, minutes=None, seconds=None, at=None):
        self.uuid = uuid
        self.task_uuid = task_uuid
        self.weeks = weeks
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.at = at

    def get_all() -> list:
        schedules = []
        for uuid in Connection.get_connection().scan_iter('schedule:*'):
            schedules.append(Connection.get_connection().json().get(f'{uuid.decode()}'))
        return schedules

    def exists(uuid) -> bool:
        return Connection.get_connection().get(f'schedule:{uuid}') != None

    def save(self) -> None:
        Connection.get_connection().json().set(f'schedule:{self.uuid}', Path.rootPath(), self.__to_json__())

    def start(self) -> bool:
        return schedule_task(self.task_uuid, weeks=self.weeks, days=self.days, hours=self.hours, minutes=self.minutes, seconds=self.seconds, at=self.at)

    def delete(uuid: str) -> None:
        Connection.get_connection().delete(f'schedule:{uuid}')

    def __to_json__(self) -> json:
        return {
            "task_uuid": self.task_uuid,
            "weeks": self.weeks,
            "days": self.days,
            "hours": self.hours,
            "minutes": self.minutes,
            "seconds": self.seconds,
            "at": self.at
        }