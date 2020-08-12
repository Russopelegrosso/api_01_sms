import time
import os
import requests

from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'v': 5.122,
        'fields': 'online',
        'access_token': os.getenv('vk_token'),
    }
    status = requests.post('https://api.vk.com/method/users.get',
                           params=params).json()['response']
    return status[0]['online']


def sms_sender(sms_text):
    client = Client(os.getenv('account_sid'), os.getenv('auth_token'))
    message = client.messages.create(
        from_=os.getenv('NUMBER_FROM'),
        body=sms_text,
        to=os.getenv('NUMBER_TO')
    )
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
