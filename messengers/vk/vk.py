import os

import vk_api
import requests
import configparser
import random
from datetime import datetime
import sys
sys.path.append("./../manage_data.py")
from manage_data import send_data

from vk_api.longpoll import VkLongPoll, VkEventType


def auth_handler():
    """При двухфакторной аутентификации вызывается эта функция"""

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device


def auth():
    # Считываем учетные данные
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'config.ini'))

    login = config['Vk']['login']
    password = config['Vk']['password']

    vk_session = vk_api.VkApi(
        login, password, app_id=2685278
        # функция для обработки двухфакторной аутентификации
    )

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    return vk_session


def send_data_to_server(data):
    """Отправляет словарь на сервер"""
    print(data)


# Отправляем сообщение
def send_message(user_id, text):
    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(-100000, +100000),
        attachment=None,
        payload=None
    )


def start_vk():
    try:
        print('START VK')
        global vk

        vk_session = auth()  # Авторизация
        vk_session.method('messages.getLongPollServer', {})
        longpoll = VkLongPoll(vk_session)
        vk = vk_session.get_api()

        # получение списка диалогов
        conversations = vk.messages.getConversations(filter='unread')

        # обработка списка диалогов
        for conversation in conversations['items']:
            # получение id диалога
            dialog_peer_id = conversation['conversation']['peer']['id']
            # получение количества непрочитанных сообщений
            unread_count = conversation['conversation']['unread_count']

            user = vk.users.get(user_ids=(str(dialog_peer_id)))[0]
            username = user['first_name'] + " " + user['last_name']

            print('Новые не обработанные сообщения:', username, dialog_peer_id, unread_count)

            history = vk.messages.getHistory(
                peer_id=dialog_peer_id,
                count=unread_count
            )

            # обработка истории сообщений
            for message in reversed(history['items']):
                message_text = message['text']
                message_date = message['date']

                data = {'id': user['id'],
                        'username': username,
                        'message': message_text,
                        'date': message_date,
                        'messenger': 'vk'}

                send_data(data)

        for event in longpoll.listen():
            try:
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    # Слушаем longpoll, если пришло сообщение то:
                    if event.from_user:  # Если написали в ЛС
                        user = vk.users.get(user_ids=(str(event.user_id)))[0]

                        data = {'id': user['id'],
                                'username': (user['first_name'], user['last_name']),
                                'message': event.message,
                                'date': event.datetime,
                                'messenger': 'vk'}

                        send_data(data)

                        # vk.messages.send(  # Отправляем сообщение
                        #     user_id=event.user_id,
                        #     message='Ваш текст'
                        #
            except Exception as e:
                print('Ошибка', e)

    except Exception as e:
        print(e)


vk = None

if __name__ == '__main__':
    start_vk()
