from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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