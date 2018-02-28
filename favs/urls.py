u"""いいねを表示する機能のview."""

from django.urls import path

from . import views

app_name = 'favs'

urlpatterns = [
    path('trial/', views.index, name='index'),
    path('trail/<int:page>/', views.index, name='index_page'),
    path('<str:screen_name>/show/', views.show, name='show'),
    path('<str:screen_name>/show/<int:page>/', views.show, name='show_page'),
    path('favorite/', views.account, name="account"),
    path('favorite/<int:page>/', views.account, name='account_page'),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('text/', views.text, name="text"),
    # path('test_masonry/', views.test_masonry, name="text_masonry"),
    path('save/confirm/<int:tweet_id>/', views.save_tweet_confirm,
         name="save_tweet_confirm"),
    path('save/<int:tweet_id>/', views.save_tweet, name="save_tweet"),
    path('top/', views.top_page, name="top_page"),
    path('', views.record, name="record"),
    path('<int:page>/', views.record, name="record_page"),
    path('delete/confirm/<int:tweet_id>/', views.delete_tweet_confirm,
         name="delete_tweet_confirm"),
    path('delete/<int:tweet_id>/', views.delete_tweet, name="delete_tweet"),
]
