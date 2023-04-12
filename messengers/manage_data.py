import requests

import asyncio
from threading import Thread
import os

import sys
sys.path.append(".")

BACKEND_SERVER = os.environ.get('BACKEND_SERVER', 'http://127.0.0.1:8000/')
LOGIN_URL = "/user/login"
REGISTER_URL = "/user/register"
PROFILE_URL = '/user/profile'
ID_USER = '/user/me'
MESSAGE_URL = "/message/message"


# ВРЕМЕННО
receiver_id = 1


def send_data(data):
    print(data)

    bearer = login(data)

    response = requests.get(BACKEND_SERVER + ID_USER, headers=bearer)
    result = response.json()

    payload = {
        "sender_id": result['user']['id'],
        "receiver_id": receiver_id,
        "message": data['message'],
    }

    # send message
    requests.post(BACKEND_SERVER + MESSAGE_URL, data=payload, headers=bearer)


def answer(data):
    try:
        if data['messenger'] == 'telegram':
            from telegram.telegram import answer_message
            loop = asyncio.new_event_loop()
            loop.run_until_complete(answer_message(data['name'], data['message']))
        elif data['messenger'] == 'vk':
            from vk.vk import send_message
            send_message(data['user_id'], data['message'])
        elif data['messenger'] == 'email':
            from mail.mail import send_email
            send_email(data['user_id'], data['message'])
    except Exception as e:
        print('Ошибка')
        print(e)


def register(data):
    print('Register')

    data_login = {
        "username": data['id'],
        "password": data['id'],
    }

    # регистрация
    reg = requests.post(BACKEND_SERVER + REGISTER_URL, data=data_login)

    # логинемся
    response = requests.post(BACKEND_SERVER + LOGIN_URL, data=data_login)
    result = response.json()
    bearer = {'Authorization': 'Bearer {}'.format(result['access'])}

    # Получаем id пользователя
    response = requests.get(BACKEND_SERVER + ID_USER, headers=bearer)
    result = response.json()

    data_profile = {
        'user_id': result["user"]["id"],
        'first_name': data['username'],
        'last_name': data['messenger']
    }

    # Формируем профиль
    profile = requests.post(BACKEND_SERVER + PROFILE_URL, data=data_profile, headers=bearer)
    return bearer


# Производим логин и возваращаем данные "access"
def login(data):
    data_login = {
        "username": data['id'],
        "password": data['id'],
    }

    response = requests.post(BACKEND_SERVER + LOGIN_URL, data=data_login)

    if response.status_code == 400:
        return register(data)
    else:
        result = response.json()
        return {'Authorization': 'Bearer {}'.format(result['access'])}


def start():
    from server import keep_alive
    serv = Thread(target=keep_alive)
    serv.start()

    from vk.vk import start_vk
    vk = Thread(target=start_vk)
    vk.start()

    from mail.mail import start_mail
    mail = Thread(target=start_mail)
    mail.start()

    # from telegram.telegram import start_tg
    # start_tg()

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())

    #  WORK
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(answer_message(991296393, 1))

    # Thread(target=answer_message, args=['1', '2']).start()
    # t = Thread(target=main)
    # t.start()


if __name__ == '__main__':
    start()
