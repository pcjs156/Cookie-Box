from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.test_view, name="test"),
    path('ex/', views.EXAMPLE_view, name="example"),
]
