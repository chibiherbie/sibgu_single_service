import configparser
import json

from telethon.sync import TelegramClient, events
import requests
from requests.auth import HTTPBasicAuth

from messengers.manage_data import send_data

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest, SendMessageRequest

from datetime import date, datetime


# Считываем учетные данные
config = configparser.ConfigParser()
config.read("../../config.ini")

# Присваиваем значения внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

# proxy = (proxy_server, proxy_port, proxy_key)

client = TelegramClient(username, api_id, api_hash)


@client.on(events.NewMessage())
async def normal_handler(event):
    """Обрабатывает сообщения"""
    # если чат, то выходим
    if event.chat:
        return

    sender = await event.get_sender()

    send_data({'id': sender.id,
               'username': sender.username,
               'message': event.message.message,
               'date': event.message.date})
    # await client(SendMessageRequest(sender.username, 'hello'))


def send_dasta(data):
    """Отправляет словарь на сервер"""
    #
    HOST = 'http://127.0.0.1:8000/'
    login_url = "user/login"
    register_url = "user/register"
    profile_url = 'user/profile'
    datas = {'username': data['id'], 'password': data['id']}
    sess = requests.Session()
    #

    response = requests.post(HOST + login_url, data={'username': data['id'], 'password': data['id']})
    if response.status_code == 400:
        print('Register')
        register = sess.post(HOST + register_url, data=datas)
        result = register.json()
        print(result)

        print('Login')
        basic = HTTPBasicAuth(datas['username'], datas['password'])
        response = sess.post(HOST + login_url, data=datas, auth=basic)
        result = response.json()
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])}
        print(result)

        response = sess.post(HOST + 'user/me')
        result = response.json()
        print(result)

        profile = requests.post(HOST + profile_url, data={'user_id': 'c', 'first_name': data['username'],
                                                          'last_name': 'telegram'}, **bearer)
        return

    # profile = requests.post(HOST + profile_url, data={'user_id': '', 'first_name': data['username'],
    #                                                   'last_name': 'telegram'})
    print('Login')
    basic = HTTPBasicAuth(datas['username'], datas['password'])
    response = sess.post(HOST + login_url, data=datas, auth=basic)
    result = response.json()
    bearer = {'Authorization': 'Bearer {}'.format(result['access'])}
    print(result)

    response = sess.get(HOST + 'user/me', headers=bearer)
    result = response.json()
    print(result)

    profile = requests.post(HOST + profile_url, data={'user_id': result["user"]["id"], 'first_name': data['username'],
                                                      'last_name': 'telegram'}, headers=bearer)
    print(profile.json())


# Запуск
client.start()
client.run_until_disconnected()


# async def main():
#     pass


# with client:
#     client.loop.run_until_complete(main())
