from django.urls import path

from . import views

app_name = 'favs'

urlpatterns = [
    # path('', views.index, name='index'),
    path('<str:screen_name>/show/', views.show, name='show'),
    # path('login/', views.login, name='login'),
    # path('callback/', views.callback, name='callback'),
    # path('logout/', views.logout, name='logout'),
]
