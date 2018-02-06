u"""oauthのテスト用."""

from django.urls import path
from . import views

app_name = 'twitterManager'

urlpatterns = [
    path('complete/', views.complete_view, name='complete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
