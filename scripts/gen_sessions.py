import re
from time import sleep

from leads.models import TGSession
from pandas import read_csv, isna
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

csv = 'scripts/sessions.csv'
data = read_csv(csv)


def get_otp(client):
    client.connect()
    messages = client.get_messages(777000, 1)
    client.disconnect()
    if messages:
        return re.findall('[0-9]+', messages[0].message)[0]
    return 'Retry'


def get_sess(client, client2, phone_number):
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        sleep(2)
        client.sign_in(phone_number, get_otp(client2))
        return client.session.save()


for n, row in data.iterrows():
    ph_num = row['number']
    if len(list(TGSession.objects.filter(phone_num=ph_num).all())) != 0:
        continue
    base_sess = row['sess_str1']
    print(ph_num)

    cl1 = TelegramClient(StringSession(base_sess), 1868530, "edf7d1e794e0b4a5596aa27c29d17eba")

    for i in range(2, 5):
        print(i)
        if isna(row[f'sess_str{i}']):
            cl2 = TelegramClient(StringSession(), 1868530, "edf7d1e794e0b4a5596aa27c29d17eba")
            try:
                sess = get_sess(cl2, cl1, ph_num)
            except Exception:
                print('Error')
                break
            data.at[n, f'sess_str{i}'] = sess
            data.to_csv(csv, index=False)
    else:
        try:
            TGSession.objects.create(phone_num=ph_num,
                                     session_str1=data.at[n, f'sess_str1'],
                                     session_str2=data.at[n, f'sess_str2'],
                                     session_str3=data.at[n, f'sess_str3'],
                                     session_str4=data.at[n, f'sess_str4'])
        except Exception:
            print('Failed')
