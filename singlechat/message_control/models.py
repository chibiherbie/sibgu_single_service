from django.db import models


class GenericFileUpload(models.Model):
    file_upload = models.FileField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_upload}"
