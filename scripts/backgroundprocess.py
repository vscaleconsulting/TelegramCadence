from datetime import timedelta

from background_task import background
from django.utils import timezone

from .functions import send_message, join_grp
 
@background(schedule=0)
def schedule_message(session, group_name, message):
    send_message(session, group_name, message)


def schedule_cadence(cadence, group_name, start_time):
    now = timezone.localtime()

    messages = cadence.messagescript_set.all()
    unique_sess = messages.values_list('account__sess_str').distinct().all()

    for sess in unique_sess:
        join_grp(group_name, sess[0])

    for message in messages:
        session = message.account.sess_str
        delay = timedelta(days=message.time_days, hours=message.time_hours,
                          minutes=message.time_minutes, seconds=message.time_seconds)
        message = message.message
        start_time += delay
        
        schedule_message(session, group_name, message, schedule=start_time - now)
        