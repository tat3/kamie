u"""いいねを表示する機能のview."""

from django.urls import path

from . import views

app_name = 'favs'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:screen_name>/show/', views.show, name='show'),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
]
