import configparser
import json

from telethon.sync import TelegramClient, events

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


def send_data(data):
    """Отправляет словарь на сервер"""
    print(data)


# Запуск
client.start()
client.run_until_disconnected()


# async def main():
#     pass


# with client:
#     client.loop.run_until_complete(main())
