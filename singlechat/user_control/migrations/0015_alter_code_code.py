# Generated by Django 4.1.3 on 2023-02-07 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_control', '0014_alter_code_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='code',
            field=models.CharField(default=['s', 'a', 'a', 's', 'a', 's'], max_length=16, unique=True),
        ),
    ]