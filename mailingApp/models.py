from django.db import models
from datetime import datetime

class TestMail(models.Model):
    class Meta:
        verbose_name = "테스트 메일"

    receiver = models.EmailField(verbose_name="주소")
    subject = models.CharField(max_length=50, verbose_name="제목")
    content = models.TextField(verbose_name="본문")
    send_date = models.DateTimeField(default=datetime.now(), verbose_name="발송 시각")
    has_been_sent = models.BooleanField(default=False, verbose_name="전송 여부")
