from . import models
from message_scripts.models import MessageScript
from random import randint
from accounts.models import Account

def create_mass_messages(messages,accounts,cadence,days,hours,minutes,seconds):
    
    
    for message in messages:
        try:
            account_id = accounts[randint(0,len(accounts)-1)]
            account = Account.objects.get(acc_id=account_id)
            MessageScript.objects.create(cadence=cadence,account=account,message=message,time_days=days,time_hours=hours,time_minutes=minutes,time_seconds=seconds)
            seconds+=0.5

        except:
            print("error log in cadence/functions.py",e)
        