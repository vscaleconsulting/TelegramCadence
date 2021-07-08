import asyncio
from datetime import datetime

from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

debug = True


def send_message(sender_session, receiver, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if debug:
        print(f'Message {message} sent to {receiver} at {datetime.now()} from {sender_session=}')
        return True

    client = TelegramClient(StringSession(sender_session),
                            1868530, "edf7d1e794e0b4a5596aa27c29d17eba", loop=loop)

    client.connect()
    try:
        client.send_message(receiver, message)
        client.disconnect()
        return True
    except Exception as e:
        print(e)
        client.disconnect()
        return False


def join_grp(grp_name, str_sess):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(StringSession(str_sess), 1868530, "edf7d1e794e0b4a5596aa27c29d17eba", loop=loop)
    with client:
        try:
            client(JoinChannelRequest(grp_name))
            return True
        except:
            return False
