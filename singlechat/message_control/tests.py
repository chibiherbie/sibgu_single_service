from rest_framework.test import APITestCase
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from six import BytesIO
from PIL import Image


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


# class TestFileUpload(APITestCase):
#     file_upload_url = '/message/file-upload'
#
#     def test_file_upload(self):
#         # определение
#
#         avatar = create_image(None, 'avatar.png')
#         avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
#         data = {
#             "file_upload": avatar_file
#         }
#
#         # Процесс
#         response = self.client.post(self.file_upload_url, data=data)
#         print(response)
#         result = response.json()
#
#         print(result)

class TestMessage(APITestCase):
    message_url = "/message/message"

    def setUp(self):
        from user_control.models import CustomUser, UserProfile

        # sender
        self.sender = CustomUser.objects._create_user('sender', 'sender123')
        UserProfile.objects.create(first_name='sender', last_name='sender', user=self.sender)

        # receiver
        self.receiver = CustomUser.objects._create_user('receiver', 'receiver123')
        UserProfile.objects.create(first_name='receiver', last_name='receiver', user=self.receiver)

        # auth
        self.client.force_authenticate(user=self.sender)

    def test_post_message(self):
        payload = {
            "sender_id": self.sender.id,
            "receiver_id": self.receiver.id,
            "message": "test message",
        }

        response = self.client.post(self.message_url, data=payload)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["message"], "test message")
        self.assertEqual(result["sender"]["user"]["username"], "sender")
        self.assertEqual(result["receiver"]["user"]["username"], "receiver")

