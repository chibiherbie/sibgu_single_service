import vk_api
import requests
import configparser


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция"""

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    """"""
    # Считываем учетные данные
    config = configparser.ConfigParser()
    config.read("../../config.ini")

    # Присваиваем значения внутренним переменным
    login = config['Vk']['login']
    password = config['Vk']['password']

    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return


if __name__ == '__main__':
    main()