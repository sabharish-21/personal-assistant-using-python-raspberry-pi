# Generated by Django 4.0.6 on 2022-07-18 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_alter_userlog_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='dateTime',
            field=models.DateTimeField(),
        ),
    ]