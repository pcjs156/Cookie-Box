from django.core.mail import EmailMessage

from apscheduler.schedulers.background import BackgroundScheduler
from .models import TestMail
from datetime import datetime

class EmailScheduler(BackgroundScheduler):
    # send 메서드 호출 시점에 전송되어야 할 메일들을 보내고, 전송했음을 표시해줌
    def send(self):
        mails = TestMail.objects.filter(send_date__range=(datetime(2000, 1, 1), datetime.now()))
        for mail in mails:
            email = EmailMessage(mail.subject, mail.content, to=[mail.receiver])
            email.send()
            mail.has_been_sent = True
            mail.save()

    # 하루의 매 hour, minute마다 이메일을 전송
    # hour: 0-23
    # minute: 0-59
    def run(self, hour=0, minute=0):
        self.add_job(self.send, 'cron', hour=hour, minute=minute)
        self.start()