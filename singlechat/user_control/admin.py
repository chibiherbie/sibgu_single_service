from django.contrib import admin

from .models import CustomUser, Jwt, Code


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
    fields = ('username', 'password', 'is_staff', 'is_superuser')
    actions = ['get_bd']
    # username.short_description = '123'

    def username(self, obj):
        print(obj)
        return obj.username

    username.short_description = 'Имя пользователя'


admin.site.register((Jwt, Code))
admin.site.register(CustomUser, CustomUserAdmin)

# admin.site.register()
admin.site.site_title = 'Админ панель SIBGU'
admin.site.site_header = 'Админ панель SIBGU'



