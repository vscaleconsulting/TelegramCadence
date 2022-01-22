from . import models
from message_scripts.models import MessageScript
from accounts.models import Account

def create_mass_messages(names,messages,cadence,days,hours,minutes,seconds):
    
    size = len(messages)

    for message_index in range(size):
        try:
            account = Account.objects.get(acc_name=names[message_index])
            MessageScript.objects.create(cadence=cadence,account=account,message=messages[message_index],time_days=days,time_hours=hours,time_minutes=minutes,time_seconds=seconds)
            seconds+=0.5

        except Exception as e:
            print("error log in cadence/functions.py",e)
        