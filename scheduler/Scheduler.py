from db.Connection import Connection
import threading
import time
import schedule
import re
from models.Task import Task
from redis.commands.json.path import Path

def run_continuously(interval=1):
    
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def schedule_exists(schedule_uuid:str):
    return Connection.get_connection().json().get(f'schedule:{schedule_uuid}') != None

def get_schedule(schedule_uuid:str):
    return Connection.get_connection().json().get(f'schedule:{schedule_uuid}')

def increment_schedule_execution(schedule_uuid:str):
    schedule = get_schedule(schedule_uuid=schedule_uuid)
    print(schedule)
    schedule["num_executions"] += 1
    Connection.get_connection().json().set(f'schedule:{schedule["uuid"]}', Path.rootPath(), schedule)

def run_task(schedule_uuid:str, task_uuid: str):
    if schedule_exists(schedule_uuid=schedule_uuid) and Task.exists(uuid=task_uuid):
        sc = get_schedule(schedule_uuid=schedule_uuid)
        if sc["num_executions"] < sc["times"]:
            Task.get(uuid=task_uuid).run()
            increment_schedule_execution(schedule_uuid=schedule_uuid)
            sc = get_schedule(schedule_uuid=schedule_uuid)
            if sc["num_executions"] == sc["times"]:
                print("reached maximum executions, quitting..")
                return schedule.CancelJob
        else:
            schedule.CancelJob
    else:
        print("task or schedule non existing, quitting..")
        return schedule.CancelJob

def stop_task(schedule_uuid: str):
    pass

def schedule_task(schedule_uuid:str, task_uuid: str, weeks=None, days=None, hours=None, minutes=None, seconds=None, at=None) -> bool:
    
    if weeks:
        if at:
            week_day, day_time = at.split(' ')[0].lower(), at.split(' ')[1].lower()
            pattern = re.compile("^[0-1][0-9]:[0-5][0-9]:[0-5][0-9]$|^[2][0-3]:[0-5][0-9]:[0-5][0-9]$")
            if pattern.match(day_time):
                if week_day == "monday":
                    schedule.every(weeks).monday.at(day_time).do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
                elif week_day == "tuesday":
                    schedule.every(weeks).tuesday.at(day_time).do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
                elif week_day == "wednesday":
                    schedule.every(weeks).wednesday.at(day_time).do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
                elif week_day == "thursday":
                    schedule.every(weeks).thursday.at(day_time).do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
                elif week_day == "friday":
                    schedule.every(weeks).friday.at(day_time).do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
                elif week_day == "saturday":
                    schedule.every(weeks).saturday.at(day_time).do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
                elif week_day == "sunday":
                    schedule.every(weeks).sunday.at(day_time).do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
                else:
                    return False
            else:
                return False
        else:
            schedule.every(weeks).weeks.do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
    elif days:
        if at:
            pattern = re.compile("^[0-1][0-9]:[0-5][0-9]:[0-5][0-9]$|^[2][0-3]:[0-5][0-9]:[0-5][0-9]$")
            if pattern.match(at):
                schedule.every(days).days.at(at).do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
            else:
                return False
        else:
            schedule.every(days).days.do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
    elif hours:
        if at:
            pattern = re.compile("^[0-5][0-9]:[0-5][0-9]$")
            if pattern.match(at):
                schedule.every(hours).hours.at(at).do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
            else:
                return False
        else:
            schedule.every(hours).hours.do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
    elif minutes:
        if at:
            pattern = re.compile("^:[0-5][0-9]$")
            if pattern.match(at):
                schedule.every(minutes).minutes.at(at).do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
            else:
                return False
        else:
            schedule.every(minutes).minutes.do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)
    elif seconds:
        schedule.every(seconds).seconds.do(run_task, schedule_uuid=schedule_uuid, task_uuid=task_uuid)

    return True

def get_active_schedules():
    schedules = []
    for uuid in Connection.get_connection().scan_iter('schedule:*'):
        schedules.append(Connection.get_connection().json().get(f'{uuid.decode()}'))
    return schedules

async def start_background_scheduler(app):
    print("############## starting main schedule thread")

    for schedule in get_active_schedules():
        print(f'####### Adding : {schedule["uuid"]}')
        schedule_task(schedule_uuid=schedule["uuid"], task_uuid=schedule["task_uuid"], weeks=schedule["weeks"], days=schedule["days"], hours=schedule["hours"], minutes=schedule["minutes"], seconds=schedule["seconds"], at=schedule["at"])

    scheduler_thread = run_continuously()
    app.ctx.scheduler_thread = scheduler_thread

async def stop_background_scheduler(app):
    print("############## stopping main schedule thread")
    scheduler_thread = app.ctx.scheduler_thread
    scheduler_thread.set()