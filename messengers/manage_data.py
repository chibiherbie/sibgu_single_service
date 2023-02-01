import requests

HOST = 'http://127.0.0.1:8000/'
LOGIN_URL = "user/login"
REGISTER_URL = "user/register"
PROFILE_URL = 'user/profile'
ID_USER = 'user/me'
MESSAGE_URL = "/message/message"

# ВРЕМЕННО
receiver_id = 5


def send_data(data):
    bearer = login(data)

    response = requests.get(HOST + ID_USER, headers=bearer)
    result = response.json()

    payload = {
        "sender_id": result['user']['id'],
        "receiver_id": receiver_id,
        "message": data['message'],
    }

    # send message
    requests.post(HOST + MESSAGE_URL, data=payload, headers=bearer)


def register(data):
    print('Register')

    data_login = {
        "username": data['id'],
        "password": data['id'],
    }

    # регистрация
    reg = requests.post(HOST + REGISTER_URL, data=data_login)

    # логинемся
    response = requests.post(HOST + LOGIN_URL, data=data_login)
    result = response.json()
    bearer = {'Authorization': 'Bearer {}'.format(result['access'])}

    # Получаем id пользователя
    response = requests.get(HOST + ID_USER, headers=bearer)
    result = response.json()

    data_profile = {
        'user_id': result["user"]["id"],
        'first_name': data['username'],
        'last_name': 'telegram'
    }

    # Формируем профиль
    profile = requests.post(HOST + PROFILE_URL, data=data_profile, headers=bearer)
    return bearer


# Производим логин и возваращаем данные "access"
def login(data):
    data_login = {
        "username": data['id'],
        "password": data['id'],
    }

    response = requests.post(HOST + LOGIN_URL, data=data_login)

    if response.status_code == 400:
        return register(data)
    else:
        result = response.json()
        return {'Authorization': 'Bearer {}'.format(result['access'])}

