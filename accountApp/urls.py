from django.urls import path

from . import views

urlpatterns = [
    path('', views.account_view, name="account_main"),
    path('auth_code_reissue/<username>', views.auth_code_reissue_view, name="auth_code_reissue"),
    path('email_modify/<username>', views.email_modify_view, name="email_modify"),
    path('logIn/', views.logIn_view, name="logIn"),
    path('logOut/', views.logOut, name="logOut"),
    path('signUp/', views.signUp_view, name="signUp"),
    path('signUp_succeeded/<username>', views.signUp_succeeded_view, name="signUp_succeeded"),
    path('unauthenticated/<username>', views.unauthenticated_view, name="unauthenticated"),
    path('edit_profile/', views.edit_profile_view, name="edit_profile"),
]
