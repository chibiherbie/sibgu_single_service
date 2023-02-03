import asyncio
import configparser
import json

from telethon.sync import TelegramClient, events

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest, SendMessageRequest

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("../config.ini")

# Присваиваем значения внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

# proxy = (proxy_server, proxy_port, proxy_key)
client = TelegramClient(username, api_id, api_hash)
loop = asyncio.get_event_loop()
# client.start()


@client.on(events.NewMessage)
async def normal_handler(event):
    """Обрабатывает сообщения"""
    # если чат, то выходим
    if event.chat:
        return

    sender = await event.get_sender()

    # ----------
    # if sender.id != 991296393:
    #     print('Не тот')
    #     return
    # ---------

    from messengers.manage_data import send_data
    loop2 = asyncio.new_event_loop()
    loop2.run_in_executor(send_data({'id': sender.id,
                                     'username': sender.username,
                                     'message': event.message.message,
                                     'date': event.message.date}))

    print('123')


async def answer_message(user_id, message):
    try:
        print('send msg')

        await client.send_message(entity=user_id, message=message)
        await client.disconnect()
        # await client(SendMessageRequest(user_id, message))

    except Exception as e:
        print(e)


# Запуск
def main():
    # loop = asyncio.new_event_loop()
    print('START TG')
    client.connect()
    client.loop.run_forever()

    # client.add_update_handler(тщ)


if __name__ == '__main__':
    main()
