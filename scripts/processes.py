import asyncio
from datetime import timedelta
from threading import Thread
from multiprocessing import Process
from asgiref.sync import sync_to_async
from pandas import read_csv
from telethon import TelegramClient
from telethon import events
from telethon.sessions import StringSession

from leads.models import TelegramMessage, TGSession, Lead
from time import sleep


def job(sess_str, ph_no):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(StringSession(sess_str), 1868530, "edf7d1e794e0b4a5596aa27c29d17eba", loop=loop)

    sess = TGSession.objects.filter(phone_num=ph_no).first()

    @sync_to_async
    def update_message(message):
        date = message.date + timedelta(hours=5, minutes=30)
        try:
            ids = list(Lead.objects.filter(telegram_id=message.peer_id.user_id).all())
            if ids:
                TelegramMessage.objects.create(message_id=message.id, tg_session=sess, from_id=message.from_id.user_id,
                                            peer_id=message.peer_id.user_id, datetime=date,
                                            message=message.message,
                                            out=message.out)
        except AttributeError:
            pass
        

    @client.on(events.NewMessage())
    async def handler(event):
        message = event.message
        print(message)
        await update_message(message)

    with client:
        client.run_until_disconnected()


USE_PROCESS = False
sessions = TGSession.objects.all()
threads = []

for session in sessions:
    session_str = session.session_str2
    number = session.phone_num
    print(number)
    if USE_PROCESS:
        threads.append(Process(target=job, args=(session_str, number)))
    else:
        threads.append(Thread(target=job, args=(session_str, number)))

for thread in threads:
    thread.start()

print("threads spawned")

try:
    while True:
        sleep(100000)
except KeyboardInterrupt:
    if USE_PROCESS:
        for thread in threads:
            thread.kill()
    else:
        exit()