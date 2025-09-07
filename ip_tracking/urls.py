from django.urls import path
from . import views

urlpatterns = [
    path('anonymous/', views.anonymous_view, name='anonymous'),
    path('login/', views.login_view, name='login'),
]