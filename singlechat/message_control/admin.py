from django.contrib import admin
from .models import Message
from import_export.admin import ExportActionMixin


class MessageAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message')

    '''
    Как можно экспортировать в ексeль без библиотеке

    actions = ['get_bd']
    @admin.action(description='Скачать все данные')
    def get_bd(self, request, queryset):
        message = Message.objects.all()
        print(message)

        response = HttpResponse(message, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="books.xls"'

        writer = csv.writer(response)
        writer.writerow(['Sender', 'Receiver', 'Message'])
        for msg in message:
            writer.writerow([msg.sender, msg.receiver, msg.message])

        return response
    '''


admin.site.register(Message, MessageAdmin)

