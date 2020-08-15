import logging
import time
import os
import requests
from requests import RequestException

from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

version_api = 5.122

url = 'https://api.vk.com/method/users.get'

acc_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
from_number = os.getenv('NUMBER_FROM')
to_number = os.getenv('NUMBER_TO')


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'v': version_api,
        'fields': 'online',
        'access_token': os.getenv('vk_token'),
    }
    try:
        status = requests.post(url, params=params).json()['response']
        return status[0]['online']
    except RequestException as err:
        logging.debug(err, "'Error getting JSON'")


def sms_sender(sms_text):
    client = Client(acc_sid, auth_token)
    message = client.messages.create(
        from_=from_number,
        body=sms_text,
        to=to_number
    )
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
