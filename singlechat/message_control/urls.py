from rest_framework.routers import DefaultRouter
from .views import GenericFiledUploadView
from django.urls import path, include


router = DefaultRouter(trailing_slash=False)

router.register("file_upload", GenericFiledUploadView)

urlpatterns = [
    path("", include(router.urls))
]
