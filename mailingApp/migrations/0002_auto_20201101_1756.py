# Generated by Django 2.2 on 2020-11-01 08:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailingApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testmail',
            name='when_to_send',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 1, 17, 56, 0, 350301), verbose_name='발송 시간'),
        ),
    ]
