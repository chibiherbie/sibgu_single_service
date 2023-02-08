# Generated by Django 4.1.3 on 2023-02-07 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_control', '0008_alter_customuser_name_alter_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='code',
            field=models.CharField(default=19, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, default='', max_length=100, unique=True),
        ),
    ]