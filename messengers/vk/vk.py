import vk_api
import requests
import configparser
import random

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
    config.read("../../config.ini")

    login = config['Vk']['login']
    password = config['Vk']['password']

    vk_session = vk_api.VkApi(
        login, password, app_id=2685278,
        auth_handler=auth_handler  # функция для обработки двухфакторной аутентификации
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
def send_message(vk, user_id, text):
    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(-100000, +100000),
        attachment=None,
        payload=None
    )


def main():
    vk_session = auth()  # Авторизация

    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            # Слушаем longpoll, если пришло сообщение то:
            if event.from_user:  # Если написали в ЛС
                user = vk.users.get(user_ids=(str(event.user_id)))[0]

                send_data_to_server({'id': user['id'],
                                     'username': (user['first_name'], user['last_name']),
                                     'message': event.message,
                                     'date': event.datetime})

                # vk.messages.send(  # Отправляем сообщение
                #     user_id=event.user_id,
                #     message='Ваш текст'
                # )


if __name__ == '__main__':
    main()
