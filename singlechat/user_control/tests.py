from rest_framework.test import APITestCase
from .views import get_random, get_refresh_token, get_access_token
from .models import CustomUser


class TestGenericFunctions(APITestCase):

    def test_get_random(self):

        rand1 = get_random(10)
        rand2 = get_random(10)
        rand3 = get_random(15)

        # Проверяем, что результат есть
        self.assertTrue(rand1)

        # Проверяем, что знач рандомные
        self.assertNotEqual(rand1, rand2)

        # Проверяем, что правильная длина
        self.assertEqual(len(rand1), 10)
        self.assertEqual(len(rand3), 15)

    def test_get_access_token(self):
        payload = {
            "id": 1,
        }

        token = get_access_token(payload)

        # Проверяем, вернётся ли токен
        self.assertTrue(token)

    def test_get_refresh_token(self):
        token = get_refresh_token()

        # Проверяем, вернётся ли токен
        self.assertTrue(token)


class TestAuth(APITestCase):
    login_url = "/user/login"
    register_url = "/user/register"
    refresh_url = "/user/refresh"

    def test_register(self):
        payload = {
            "username": "privet",
            "password": "qwerty"
        }

        response = self.client.post(self.register_url, data=payload)

        # Проверяем статус 201
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        payload = {
            "username": "privet",
            "password": "qwerty"
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

    def setUp(self):
        self.user = CustomUser.objects.create(username='Bronamer', password='qwerty')
        self.client.force_authenticate(user=self.user)

    def test_post_user_profile(self):

        payload = {
            "user_id": self.user.id,
            "first_name": "Roman",
            "last_name": "Bekker",
        }

        response = self.client.post(self.profile_url, data=payload)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['first_name'], "Roman")
        self.assertEqual(result['last_name'], "Bekker")
        self.assertEqual(result['user']['username'], "Bronamer")

    def test_post_user_profile_with_picture(self):

        payload = {
            "user_id": self.user.id,
            "first_name": "Roman",
            "last_name": "Bekker",
        }

        response = self.client.post(self.profile_url, data=payload)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['first_name'], "Roman")
        self.assertEqual(result['last_name'], "Bekker")
        self.assertEqual(result['user']['username'], "Bronamer")

