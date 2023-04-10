


def create_telethon_session():
    from telethon.sync import TelegramClient

    # создание клиента для работы с Telegram API c указанием пути к файлу с сессией 
    client = TelegramClient(session_name, api_id, api_hash) 

    # проверка наличия сессии, если сессия уже сохранена, авторизация не требуется
    if not client.is_user_authorized():
        client.start(phone_number)

    return client


if __name__ == '__main__':
    create_telethon_session()