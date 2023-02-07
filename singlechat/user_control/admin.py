from django.contrib import admin
from .models import CustomUser, Jwt, Code

admin.site.register((CustomUser, Jwt, Code))