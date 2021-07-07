import asyncio

from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

# str_sess = '1BJWap1wBuyQt6OZn8WsChZn6vNywyh9BfA3Z-wJ1S3mtnHR8VaO4A1uEy0YWGQDJ4dgjgn2hiN4ta28RpV-0-PKzOltZwv8oyYfz_NMfio7K98RpFD3cFBA8CVJB71LA1pmQmPJvlfomtKZJpRrQYfS2UAUfU1vXPXUVCQ2zeyMsF0d5XRkh9W6SWsabIQ5t8GGeRNpVygvu8p_ah2_SKkB4cmhKkVyObgaZQWyoosljbqUFNVtnGKx5MN7Y9pnrhCOkQeoin-cA1CmAM7kAC_hbRE287TG8nSp9um1VK-6tbYLqA_of6V0Qe63pDAkAnfp1PZv7e7ZrBm7X5vQYy5NWw2OjOIQ='


# str_sess = '1BJWap1sBu5RlcXkQ38s8SvEyt7t2ZRIlmhjoBqS61tRuFjuFPl6_gY1plGN8av0WnG4pNyfymJdhBmwm9X21m1MXJMwV9T9nPAVavrM02KrXggCBEfsvoxwQNR9MJLIs2yub0OcSkcSBtxIatCl-x664aLWFhP15A9sFBxBrN2tEtDLtUk8DLj2_GvhbYb2-hZ0uT1I7SwfRbpzw0Bufij3-5pq5mu_gub-q8EIuh3W8OAx1lmgdm2ale0H2__fSc1BnwxurpZ9MUIbs29zAkkkkeqL_dSxcuRpHCJhVj9GEvXJMGaTrQ-hTpatAoOJ-looh5pHIAgjLA89hRfxUp-nzCsiP5gw='
str_sess = '1AZWarzQBuxUGTBaDhHKOm1dSGEcnIFEE0ZwJk37cMSlvP33eyNveXN3ho4WJBiROAsfAz_aPsPOQAL1a4jc6HLBd4lh36MKoAoNT0YDT09j5Xvqv1awfqppZPWU9KpgRR2xlnIZ8DcsKGwEe-0L8LG4KMO2eQGOLrjXB_GwePKNsfaNQWXOYryk1Rf_3raI6YZ_V5hEeFv4m9s5a6L5DTOnd9BlaQkS06x1wqY1G8ilvfx1Fv4bu3PHuaeiW-8GWu6mdzdOkwCcccnryKKpAX3kHqxs-gzvCw6GJYWvNiinHx18vO-Q9YyVl1zV0LW_8SC6EOO_TKayy2ZC1bGpnh-WE6egmbms='


def get_uid(username):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(StringSession(str_sess), 1868530, "edf7d1e794e0b4a5596aa27c29d17eba", loop=loop)
    with client:
        try:
            entity = client.get_entity(username)
            try:
                grp = entity.megagroup
                return {'group': entity.id}
            except AttributeError:
                return {'user': entity.id}
        except Exception as e:
            return e


def join_grp(grp_name):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(StringSession(str_sess), 1868530, "edf7d1e794e0b4a5596aa27c29d17eba", loop=loop)
    with client:
        try:
            client(JoinChannelRequest(grp_name))
            return True
        except:
            return False
