u"""oauthのテスト用."""

# from django.contrib import admin
from django.urls import path
from django.conf.urls import include
# import django.contrib.auth.views

from . import views

urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    path('complete/', views.complete_view, name="complete"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
