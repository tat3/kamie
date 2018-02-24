u"""いいねを表示する機能のview."""

from django.urls import path

from . import views

app_name = 'favs'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>/', views.index, name='index_page'),
    path('<str:screen_name>/show/', views.show, name='show'),
    path('<str:screen_name>/show/<int:page>/', views.show, name='show_page'),
    path('account/', views.account, name="account"),
    path('account/<int:page>/', views.account, name='account_page'),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('text/', views.text, name="text"),
    # path('test_masonry/', views.test_masonry, name="text_masonry"),
    path('save/confirm/<int:tweet_id>/', views.save_tweet_confirm,
         name="save_tweet_confirm"),
    path('save/<int:tweet_id>/', views.save_tweet, name="save_tweet"),
    path('top/', views.top_page, name="top_page"),
    path('record/', views.record_likes, name="record_likes"),
]
