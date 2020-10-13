from django.urls import path

from . import views

urlpatterns = [
    path('report/', views.report_view, name="report"),
    path('schedule/', views.schedule_view, name="schedule"),
    path('statistics/', views.statistics_view, name="statistics"),
    path('subscription_list/',
         views.subscription_list_view,
         name="subscription_list"),
]
