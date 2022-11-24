from rest_framework.viewsets import ModelViewSet
from .serialezers import GenericFileUpload, GenericFileUploadSerializer


class GenericFiledUploadView(ModelViewSet):
    queryset = GenericFileUpload.objects.all()
    serialezer_class = GenericFileUploadSerializer
