# Generated by Django 2.2 on 2020-11-01 08:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestMail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.EmailField(max_length=254, verbose_name='수신자')),
                ('subject', models.CharField(default='테스트 이메일 제목', max_length=50, verbose_name='제목')),
                ('content', models.TextField(default='Test Email contents', verbose_name='본문')),
                ('when_to_send', models.DateTimeField(default=datetime.datetime(2020, 11, 1, 17, 11, 25, 179166), verbose_name='발송 시간')),
            ],
            options={
                'verbose_name': '테스트 이메일',
            },
        ),
    ]
