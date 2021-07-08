from background_task import background
from datetime import timedelta, timezone, tzinfo, datetime
from django.utils import timezone
from cadence import models
from .functions import send_message


@background(schedule=0)
def schedule_message(session, group_name, message):
    send_message(session, group_name, message)


def schedule_cadence(cadence, group_name, start_time):
    print('Scheduling')
    now = datetime.now() - timedelta(hours=12)
    now = now.replace(tzinfo=None)
    start_time = start_time.replace(tzinfo=None)
    messages = cadence.messagescript_set.all()
    delay = timedelta(seconds=0)
    for message in messages:
        session = message.account.sess_str
        delay = timedelta(days=message.time_days, hours=message.time_hours,
                                   minutes=message.time_minutes, seconds=message.time_seconds)
        message = message.message
        start_time += delay
        print(start_time, start_time.tzinfo)
        print(now, now.tzinfo)
        print(start_time-now)
        schedule_message(session, group_name, message, schedule=start_time-now)
