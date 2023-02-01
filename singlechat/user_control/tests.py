from rest_framework.test import APITestCase
from .views import get_random, get_refresh_token, get_access_token
from .models import CustomUser, UserProfile


# class TestGenericFunctions(APITestCase):
#
#     def test_get_random(self):
#
#         rand1 = get_random(10)
#         rand2 = get_random(10)
#         rand3 = get_random(15)
#
#         # Проверяем, что результат есть
#         self.assertTrue(rand1)
#
#         # Проверяем, что знач рандомные
#         self.assertNotEqual(rand1, rand2)
#
#         # Проверяем, что правильная длина
#         self.assertEqual(len(rand1), 10)
#         self.assertEqual(len(rand3), 15)
#
#     def test_get_access_token(self):
#         payload = {
#             "id": 1,
#         }
#
#         token = get_access_token(payload)
#
#         # Проверяем, вернётся ли токен
#         self.assertTrue(token)
#
#     def test_get_refresh_token(self):
#         token = get_refresh_token()
#
#         # Проверяем, вернётся ли токен
#         self.assertTrue(token)


class TestAuth(APITestCase):
    login_url = "/user/login"
    register_url = "/user/register"
    refresh_url = "/user/refresh"

    def test_register(self):
        payload = {
            "username": "privet",
            "password": "qwerty",
            "is_staff": True
        }

        response = self.client.post(self.register_url, data=payload)

        # Проверяем статус 201
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        payload = {
            "username": "privet",
            "password": "qwerty",
        }

        # reg
        self.client.post(self.register_url, data=payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        result = response.json()

        # Проверяем статус 200
        self.assertEqual(response.status_code, 200)

        # проверяем токен
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def test_refresh(self):
        payload = {
            "username": "privet",
            "password": "qwerty"
        }

        # reg
        self.client.post(self.register_url, data=payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        refresh = response.json()["refresh"]

        response = self.client.post(self.refresh_url, data={"refresh": refresh})
        result = response.json()

        self.assertEqual(response.status_code, 200)

        # проверяем токен
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])


class TestUserInfo(APITestCase):
    profile_url = '/user/profile'
    file_upload_url = '/message/file-upload'
    login_url = "/user/login"

    def setUp(self):
        payload = {
            "username": "Bronamer",
            "password": "qwerty",
        }

        self.user = CustomUser.objects._create_user(**payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        result = response.json()

        self.bearer = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])}

    def test_post_user_profile(self):

        payload = {
            "user_id": self.user.id,
            "first_name": "Roman",
            "last_name": "Bekker",
        }

        response = self.client.post(self.profile_url, data=payload, **self.bearer)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['first_name'], "Roman")
        self.assertEqual(result['last_name'], "Bekker")
        self.assertEqual(result['user']['username'], "Bronamer")

    # def test_post_user_profile_with_picture(self):
    #
    #     payload = {
    #         "user_id": self.user.id,
    #         "first_name": "Roman",
    #         "last_name": "Bekker",
    #     }
    #
    #     response = self.client.post(self.profile_url, data=payload)
    #     result = response.json()
    #
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(result['first_name'], "Roman")
    #     self.assertEqual(result['last_name'], "Bekker")
    #     self.assertEqual(result['user']['username'], "Bronamer")

    def test_update_user_profile(self):
        # создаём профиль
        payload = {
            "user_id": self.user.id,
            "first_name": "Roman",
            "last_name": "Bekker",
        }

        response = self.client.post(self.profile_url, data=payload, **self.bearer)
        result = response.json()

        payload = {
            "first_name": "Rom",
            "last_name": "Bek",
        }

        response = self.client.patch(self.profile_url + f'/{result["id"]}', data=payload, **self.bearer)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['first_name'], "Rom")
        self.assertEqual(result['last_name'], "Bek")
        self.assertEqual(result['user']['username'], "Bronamer")

    def test_user_search(self):

        UserProfile.objects.create(user=self.user, first_name="Roman", last_name="Bekker")

        user2 = CustomUser.objects._create_user(username='tester', password='tester123')
        UserProfile.objects.create(user=user2, first_name="Mega", last_name="Torch")

        user3 = CustomUser.objects._create_user(username='Rommchek', password='bulka123')
        UserProfile.objects.create(user=user3, first_name="Big", last_name="Rocket")

        # test keyword = Roman Bekker
        url = self.profile_url + "?keyword=Roman Bekker"

        responce = self.client.get(url, **self.bearer)
        result = responce.json()["results"]

        self.assertEqual(responce.status_code, 200)
        self.assertEqual(len(result), 0)

        # test keyword = rom
        url = self.profile_url + "?keyword=rom"

        responce = self.client.get(url, **self.bearer)
        result = responce.json()["results"]

        self.assertEqual(responce.status_code, 200)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["user"]["username"], "Rommchek")
