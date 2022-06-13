from sanic import Sanic, json
from sanic.log import logger
from db.Connection import Connection
import threading
import time
import schedule
import re
from models.Action import Action
from redis.commands.json.path import Path
from datetime import datetime

def run_continuously(interval=1):
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(self):
            while not cease_continuous_run.is_set():
                #sc_number = reload_active_schedules()
                #logger.info(f"Reloading schedules... {sc_number} found!")
                logger.info(f"Scheduler Jobs count:... {len(schedule.get_jobs())}")
                schedule.run_pending()
                time.sleep(interval)

    scheduler_thread = ScheduleThread()
    scheduler_thread.start()

    return cease_continuous_run

def start_scheduler_reload_thread(interval=1):
    cease_scheduler_reload_thread = threading.Event()
    class ScheduleReloaderThread(threading.Thread):
        @classmethod
        def run(self):
            while not cease_scheduler_reload_thread.is_set():
                sc_number = reload_active_schedules()
                logger.info(f"{self.name} Reloading schedules... {sc_number} found!")
                time.sleep(interval)

    scheduler_reload_thread = ScheduleReloaderThread()
    scheduler_reload_thread.start()
    
    return cease_scheduler_reload_thread

def schedule_exists(schedule_uuid:str):
    return Connection.get_connection().json().get(f'schedule:{schedule_uuid}') != None

def get_schedule(schedule_uuid:str):
    return Connection.get_connection().json().get(f'schedule:{schedule_uuid}')

def increment_schedule_execution(schedule_uuid:str):
    schedule = get_schedule(schedule_uuid=schedule_uuid)
    schedule["num_executions"] += 1
    Connection.get_connection().json().set(f'schedule:{schedule["uuid"]}', Path.rootPath(), schedule)

def run_action(schedule_uuid:str, action_uuid: str):
    if schedule_exists(schedule_uuid=schedule_uuid) and Action.exists(uuid=action_uuid):
        sc = get_schedule(schedule_uuid=schedule_uuid)
        if sc["times"] > 0:
            if sc["num_executions"] < sc["times"] and sc["enabled"]:
                Action.get(uuid=action_uuid).run()
                increment_schedule_execution(schedule_uuid=schedule_uuid)
                sc = get_schedule(schedule_uuid=schedule_uuid)
                if sc["num_executions"] == sc["times"]:
                    logger.info("Reached maximum executions, quitting..")
                    return schedule.CancelJob
                else:
                    logger.info(f"Schedule {schedule_uuid} ran {sc['num_executions']} out of {sc['times']}")
            else:
                return schedule.CancelJob
        else:
            if sc["enabled"]:
                Action.get(uuid=action_uuid).run()
                increment_schedule_execution(schedule_uuid=schedule_uuid)
                sc = get_schedule(schedule_uuid=schedule_uuid)
                print(f"Action {action_uuid} ran {sc['num_executions']} out of unlimited")
            else:
                return schedule.CancelJob
    else:
        print("Action or schedule non existing, quitting..")
        return schedule.CancelJob

def stop_action(schedule_uuid: str):
    pass

def schedule_action(schedule_uuid:str, action_uuid: str, weeks=None, days=None, hours=None, minutes=None, seconds=None, at=None) -> bool:
    
    if weeks:
        if at:
            week_day, day_time = at.split(' ')[0].lower(), at.split(' ')[1].lower()
            pattern = re.compile("^[0-1][0-9]:[0-5][0-9]:[0-5][0-9]$|^[2][0-3]:[0-5][0-9]:[0-5][0-9]$")
            if pattern.match(day_time):
                if week_day == "monday":
                    schedule.every(weeks).monday.at(day_time).do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
                elif week_day == "tuesday":
                    schedule.every(weeks).tuesday.at(day_time).do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
                elif week_day == "wednesday":
                    schedule.every(weeks).wednesday.at(day_time).do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
                elif week_day == "thursday":
                    schedule.every(weeks).thursday.at(day_time).do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
                elif week_day == "friday":
                    schedule.every(weeks).friday.at(day_time).do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
                elif week_day == "saturday":
                    schedule.every(weeks).saturday.at(day_time).do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
                elif week_day == "sunday":
                    schedule.every(weeks).sunday.at(day_time).do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
                else:
                    return False
            else:
                return False
        else:
            schedule.every(weeks).weeks.do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
    elif days:
        if at:
            pattern = re.compile("^[0-1][0-9]:[0-5][0-9]:[0-5][0-9]$|^[2][0-3]:[0-5][0-9]:[0-5][0-9]$")
            if pattern.match(at):
                schedule.every(days).days.at(at).do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
            else:
                return False
        else:
            schedule.every(days).days.do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
    elif hours:
        if at:
            pattern = re.compile("^[0-5][0-9]:[0-5][0-9]$")
            if pattern.match(at):
                schedule.every(hours).hours.at(at).do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
            else:
                return False
        else:
            schedule.every(hours).hours.do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
    elif minutes:
        if at:
            pattern = re.compile("^:[0-5][0-9]$")
            if pattern.match(at):
                schedule.every(minutes).minutes.at(at).do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
            else:
                return False
        else:
            schedule.every(minutes).minutes.do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)
    elif seconds:
        schedule.every(seconds).seconds.do(run_action, schedule_uuid=schedule_uuid, action_uuid=action_uuid)

    return True

def get_active_schedules():
    schedules = []
    for uuid in Connection.get_connection().scan_iter('schedule:*'):
        sc = Connection.get_connection().json().get(f'{uuid.decode()}')
        if sc["enabled"] and (sc["times"] < 0 or sc["num_executions"] < sc["times"]):
            schedules.append(sc)
    return schedules

def reload_active_schedules():
    scs = get_active_schedules()
    active_count = 0
    for sc in scs:
        if not sc["loaded"]:
            schedule_action(schedule_uuid=sc["uuid"], action_uuid=sc["action_uuid"], weeks=sc["weeks"], days=sc["days"], hours=sc["hours"], minutes=sc["minutes"], seconds=sc["seconds"], at=sc["at"])
            logger.info(f'Adding Scheduler : {sc["uuid"]}')
            sc["loaded"] = True
            Connection.get_connection().json().set(f'schedule:{sc["uuid"]}', Path.rootPath(), sc)
            logger.info(f'Updating Scheduler state to LOADED : {sc["uuid"]}')
            active_count+=1
        else:
            logger.info(f'Schedule {sc["uuid"]} already loaded..')
    return active_count

def unload_schedules():
    scs = get_active_schedules()
    for sc in scs:
        if sc["loaded"]:
            sc["loaded"] = False
            Connection.get_connection().json().set(f'schedule:{sc["uuid"]}', Path.rootPath(), sc)
            logger.info(f'Updating Scheduler state to UNLOADED : {sc["uuid"]}')

async def start_background_scheduler(app):
    logger.info("Starting main schedule thread...")
    reload_active_schedules()    
    scheduler_thread = run_continuously()
    scheduler_reload_thread = start_scheduler_reload_thread()
    app_t = Sanic.get_app()
    app_t.ctx.scheduler_thread = scheduler_thread
    app_t.ctx.scheduler_reload_thread = scheduler_reload_thread

async def stop_background_scheduler(app):
    logger.info("Stopping main schedule thread...")
    app_t = Sanic.get_app()
    scheduler_thread = app_t.ctx.scheduler_thread
    scheduler_reload_thread = app_t.ctx.scheduler_reload_thread
    unload_schedules()
    scheduler_thread.set()
    scheduler_reload_thread.set()
