from rest_framework.viewsets import ModelViewSet
from .serialezers import GenericFileUpload, GenericFileUploadSerializer


class GenericFileUploadView(ModelViewSet):
    queryset = GenericFileUpload.objects.all()
    serialezer_class = GenericFileUploadSerializer
