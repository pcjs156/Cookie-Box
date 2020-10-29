from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from Cookie_Box.settings import DEBUG, EMAIL_HOST_USER

# 아래는 테스트용 코드로, DEBUG 모드가 True이며 접속 계정이 staff일 때만 작동합니다.
@login_required(login_url='/account/logIn/')
def email_test_view(request):
    content = dict()

    if not DEBUG or not request.user.is_staff:
        content["DEBUG"] = False

    else:
        content["DEBUG"] = True

    return render(request, "email_test.html", content)

@login_required(login_url='/account/logIn/')
def instant_mail_send_test_view(request):
    content = dict()

    if not DEBUG or not request.user.is_staff:
        content["DEBUG"] = False

    else:
        content["DEBUG"] = True
        if request.method == "POST":
            # 수신 이메일 주소
            receiver_address = request.POST["email_address"]
            # 메일 제목
            mail_subject = "테스트 메일: 즉시 보내기"
            # 메일 내용: test_mail.html
            mail_content = render_to_string("test_mail.html")
            # TODO: 이메일 템플릿이 제대로 첨부되지 않음(태그가 노출됨)
            # 이메일 객체 생성 / 전송
            email = EmailMultiAlternatives(subject=mail_subject, from_email=EMAIL_HOST_USER,
                                           to=[receiver_address], body='??')
            email.attach_alternative(mail_content, "text/html")
            email.send()

    return render(request, "instant_mail_send_test.html", content)

# ========================================================

#  신고 내역 관리 페이지
@login_required(login_url='/account/logIn/')
def report_view(request):
    return render(request, "report.html")


# 이메일 발송 스케줄 조정 페이지
@login_required(login_url='/account/logIn/')
@login_required(login_url='/account/logIn/')
def schedule_view(request):
    return render(request, "schedule.html")


# 구독 통계 페이지
@login_required(login_url='/account/logIn/')
@login_required(login_url='/account/logIn/')
def statistics_view(request):
    return render(request, "statistics.html")


# 구독 웹진 목록 관리 페이지
@login_required(login_url='/account/logIn/')
@login_required(login_url='/account/logIn/')
def subscription_list_view(request):
    return render(request, "subscription_list.html")