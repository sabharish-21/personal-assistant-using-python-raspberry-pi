# Generated by Django 4.0.6 on 2022-07-18 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='userLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.TextField(max_length=70)),
                ('userID', models.TextField(max_length=20)),
                ('action', models.TextField(max_length=50)),
                ('dateTime', models.DateTimeField()),
            ],
        ),
    ]
