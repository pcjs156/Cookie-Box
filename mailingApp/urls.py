from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.email_test_view, name="email_test"),
    path('test/instant_mail/', views.instant_mail_send_test_view, name="instant_mail_send_test"),
    path('report/', views.report_view, name="report"),
    path('schedule/', views.schedule_view, name="schedule"),
    path('statistics/', views.statistics_view, name="statistics"),
    path('subscription_list/', views.subscription_list_view, name="subscription_list"),
]
