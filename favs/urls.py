u"""いいねを表示する機能のview."""

from django.urls import path

from . import views

app_name = 'favs'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>/', views.index, name='index_page'),
    path('<str:screen_name>/show/', views.show, name='show'),
    path('<str:screen_name>/show/<int:page>/', views.show, name='show_page'),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
]
