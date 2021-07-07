from telethon import TelegramClient
from telethon.sessions import StringSession

client = TelegramClient(StringSession('1AZWarzgBu8RY0vJK0EUAtTeLqcU0bmsoz30we4C8uFzLssfr1TZqp34LTUPP7cqqDauTalfRDdxvmfX0r1uxyz3fV2gmt38WCRQlbdZxshCSrg2Ki6khh--Coeq-bBfeCgJJg0tcNUb1-8oetAyPaV9siNXaJ_1vXzBj6mWi7wxfMzS0Es6VpL12iOq9iJ4eq_2TY2HW7DhLYVGXgdS1pRF54ThCeKVAtEeNtB4nhUgZLVQSKtSSFBilVMdT4PX_n-6dy930u_GtC7IetgOGgfPp-j5RfyI7tWgmBa4J-6sAYJQHLhlt7N8VFIrx_RE0rHROgsSExK_YvOpiIpYv2SOPBWhRVIU='), 1868530, "edf7d1e794e0b4a5596aa27c29d17eba", sequential_updates=True)


async def main():
    print(await client.get_me())


with client:
    client.loop.run_until_complete(main())
