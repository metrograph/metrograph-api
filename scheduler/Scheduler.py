# v0.0.1

# - once (takes a time -> should be in the future)
# - schedule (takes a cron -> should be a valid cron)

# v0.0.2

# - takes another task id (predecessor - runs after it -> needs to be a valid and planned task)

import threading
import time
import schedule
import re
from models.Task import Task


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
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


def background_task(task_uuid: str):
    if Task.exists(uuid=task_uuid):
        Task.get(uuid=task_uuid).run()
        print(f'Running Task {task_uuid}')
    else:
        print('task not found')

def schedule_task(task_uuid: str, days=None, hours=None, minutes=None, seconds=None, at=None) -> bool:
    
    if days:
        if at:
            pattern = re.compile("^[0-1][0-9]:[0-5][0-9]:[0-5][0-9]$|^[2][0-3]:[0-5][0-9]:[0-5][0-9]$")
            if pattern.match(at):
                schedule.every(days).days.at(at).do(background_task, task_uuid=task_uuid)
            else:
                return False
    elif hours:
        if at:
            pattern = re.compile("^[0-5][0-9]:[0-5][0-9]$")
            if pattern.match(at):
                schedule.every(hours).hours.at(at).do(background_task, task_uuid=task_uuid)
            else:
                return False
    elif minutes:
        if at:
            pattern = re.compile("^:[0-5][0-9]$")
            if pattern.match(at):
                schedule.every(minutes).minutes.at(at).do(background_task, task_uuid=task_uuid)
            else:
                return False
    elif seconds:
        schedule.every(seconds).seconds.do(background_task, task_uuid=task_uuid)

    # Start the background thread
    stop_run_continuously = run_continuously()
    return True

    # Do some other things...
    #time.sleep(5)

    # Stop the background thread
    #stop_run_continuously.set()


def start_scheduler():
    stop_run_continuously = run_continuously()
    return stop_run_continuously
