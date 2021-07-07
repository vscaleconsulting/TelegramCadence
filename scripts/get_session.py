from telethon import TelegramClient
from telethon.sessions import StringSession

client = TelegramClient(StringSession(), 1868530, "edf7d1e794e0b4a5596aa27c29d17eba", sequential_updates=True)


async def main():
    print(client.session.save())


with client:
    client.loop.run_until_complete(main())
