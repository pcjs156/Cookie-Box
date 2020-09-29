from django.urls import path

from . import views

urlpatterns = [
    path('logIn/', views.logIn_view, name="logIn"),
    path('logOut/', views.logOut, name="logOut"),
    path('unauthenticated/<username>',
         views.unauthenticated_view,
         name="unauthenticated"),
    path('signUp_succeeded/<username>',
         views.signUp_succeeded_view,
         name="signUp_succeeded"),
    path('signUp/', views.signUp_view, name="signUp"),
    path('email_modify/<username>',
         views.email_modify_view,
         name="email_modify"),
]
