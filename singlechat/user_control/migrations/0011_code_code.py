# Generated by Django 4.1.3 on 2023-02-07 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_control', '0010_code_remove_customuser_code_alter_customuser_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='code',
            field=models.CharField(default='123456', max_length=100, unique=True),
        ),
    ]
