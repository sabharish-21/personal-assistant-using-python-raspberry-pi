# Generated by Django 4.0.6 on 2022-07-18 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_alter_userlog_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlog',
            name='logID',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
