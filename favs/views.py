u"""いいねしたツイートを表示する."""

import os
import json
import datetime
from pytz import timezone

from django.shortcuts import render
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
)
from django.template import loader, Library
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage

from social_django.models import UserSocialAuth

from . import utils
from favs.models import Fav, Like

# Create your views here.

app_name = 'favs'
register = Library()

not_superuser = user_passes_test(lambda u: not u.is_superuser)


def template_path(name):
    u"""テンプレートファイル名からにapp_nameを追加."""
    return os.path.join(app_name, name)
    # return app_name + ':' + name


def redirect_favs_root():
    u"""favsのルートにリダイレクトする."""
    return HttpResponseRedirect(template_path('index.html'))


def list_items(request, user_id, page, create_page_url,
               method='like', context={}):
    u"""いいねを表示."""
    user_token = {}
    if request.user.is_authenticated:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
        user_token = user.access_token

    twitter = utils.TwitterClient(user=user_token)

    if method == 'like':
        try:
            tweets = twitter.favlist(user_id, page)
        except:
            tweets = []
    elif method == 'like_pop':
        try:
            tweets = sorted(twitter.favlist(user_id, page, count=200),
                            key=lambda tw: -tw["favorite_count"])[:10]
        except:
            tweets = []
    elif method == 'fav_db':
        qs_tweets = Fav.objects.filter(user=user).order_by("-created_at")
        p = Paginator(qs_tweets, 100)
        try:
            qs_tweets = p.page(page).object_list
        except EmptyPage:
            qs_tweets = []
        tweets = [tw.to_dict() for tw in qs_tweets]

    elif method == 'like_db':
        qs_tweets = Like.objects.filter(user=user).order_by("-created_at")
        p = Paginator(qs_tweets, 100)
        try:
            qs_tweets = p.page(page).object_list
        except EmptyPage:
            qs_tweets = []
        tweets = [tw.to_dict() for tw in qs_tweets]

    tweets = [item for item in tweets if 'media' in item['entities']]
    # tweets = twitter.add_htmls_embedded(tweets)
    # print(tweets[0]['entities']['media'])

    url_split = request.build_absolute_uri().split("/")
    base_url = url_split[0] + '//' + url_split[2]

    context = utils.merge_two_dicts(context, {
        'user': request.user,
        'tweets': tweets,
        'base_url': base_url,
        'is_pc': utils.is_pc(request),
        'create_page_url': create_page_url,
        'page': page,
        'paginator_required': True,
    })
    return context
    # return render(request, template_path('show.html'), context)
    # return HttpResponse(template.render(context, request))


def top_page(request):
    u"""ログインしていない場合のトップページ."""
    logout(request)
    return information(request, 'index')


@login_required
@not_superuser
def index(request, page=1):
    u"""ユーザーのいいねをAPIから表示."""
    user = UserSocialAuth.objects.get(user_id=request.user.id).access_token
    context = {
    }
    context = list_items(
        request, user['user_id'], page,
        lambda p: reverse('favs:index_page', kwargs={'page': p}),
        'like', context
    )
    if context["tweets"] == []:
        context['message_required'] = True
        context['messages'] = [
            {"title": "いいねが見つかりません",
             "body": "遡れるツイート数の上限かもしれません。前のページに戻ってください。"},
        ]

    return render(request, template_path('show.html'), context)


def show(request, screen_name, page=1):
    u"""指定したユーザーのいいねを表示."""
    if request.user.is_anonymous:
        twitter = utils.TwitterClient()
    else:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
        user = user.access_token
        twitter = utils.TwitterClient(user)

    # user_id = '1212759744'
    try:
        user_id = twitter.user_id_from_screen_name(screen_name)
    except:
        print(twitter.AT, twitter.AS)
        return HttpResponseNotFound('<h1>User was not found.</h1>')

    context = {
    }
    context = list_items(
        request, user_id, page,
        lambda p: reverse('favs:show_page',
                          kwargs={'screen_name': screen_name, 'page': p}),
        'like', context
    )
    if context["tweets"] == []:
        context['message_required'] = True
        context['messages'] = [
            {"title": "いいねが見つかりません",
             "body": "遡れるツイート数の上限かもしれません。前のページに戻ってください。"},
        ]

    return render(request, template_path('show.html'), context)


def information(request, name):
    u"""json内の情報を表示する."""
    contents = json.load(open('favs/json/{}.json'.format(name), 'r'))
    context = {
        'user': request.user,
        'contents': contents,
        'request': request,
    }
    return render(request, template_path('{}.html'.format(name)), context)


@login_required
@not_superuser
def account(request, page=1):
    u"""このアプリ上でfavしたツイートを表示."""
    user = UserSocialAuth.objects.get(user_id=request.user.id).access_token
    context = {
    }
    context = list_items(
        request, user['user_id'], page,
        lambda p: reverse('favs:account_page', kwargs={'page': p}),
        'fav_db', context
    )
    if context['tweets'] == []:
        context = list_items(
            request, user['user_id'], page,
            lambda p: reverse('favs:account_page', kwargs={'page': p}),
            'like_pop', context
        )
        context['paginator_required'] = False
        context['message_required'] = True
        context['messages'] = [
            {"title": "まだお気に入りが登録されていません",
             "body": "まずはあなたがいいねしたツイートからいくつかをお気に入り登録してみましょう。"},
        ]

    return render(request, template_path('show.html'), context)
    # return information(request, 'account')


def contact(request):
    u"""Contact usを表示."""
    return information(request, 'contact')


def about(request):
    u"""About usを表示."""
    return information(request, 'about')


def text(request):
    u"""テスト用."""
    return HttpResponseNotFound('<h1>Test Text.</h1>')


def test_masonry(request):
    u"""masonry.jsのテスト."""
    template = loader.get_template(template_path('test_masonry.html'))
    context = {
    }
    return HttpResponse(template.render(context, request))


@login_required
def save_tweet_confirm(request, tweet_id):
    u"""ユーザーのお気に入り登録を確認."""
    return save_tweet(request, tweet_id, confirm=True)


@login_required
def save_tweet(request, tweet_id, confirm=False):
    u"""ユーザーのお気に入りを登録."""
    tweet_id = str(tweet_id)

    user = UserSocialAuth.objects.get(user_id=request.user.id)
    twitter = utils.TwitterClient(user.access_token)

    try:
        tweet = twitter.tweet_from_id(tweet_id)
    except:
        return HttpResponseNotFound('<h1>Tweet does not exist.</h1>')

    if not Fav.objects.filter(tweet_id=tweet_id, user=user).count() == 0:
        return HttpResponseNotFound('<h1>Tweet is already saved.</h1>')

    if not confirm:
        Fav.create_item(tweet, user).save()
        return HttpResponse("<script>window.close()</script>")

    contents = [
        {'title': 'ツイートをお気に入り登録する',
         'body': ('良ければ確認ボタンを押してください。<br>'
                  'お気に入りしたツイートは<a href="/account/">アカウント画面</a>から確認できます。')},
        {'title': '{name}@{screen_name}'.format(
            name=tweet['user']['name'],
            screen_name=tweet['user']['screen_name']),
         'body': tweet['text']},
    ]
    context = {
        'contents': contents,
        'tweet_id': tweet_id,
    }
    return render(request, template_path('save_tweet.html'), context)


@login_required
@not_superuser
def record_likes(user):
    u"""ユーザーのすべてのいいねをDBに記録する."""
    twitter = utils.TwitterClient(user=user.access_token)
    user_id = user.access_token["user_id"]

    # 全てのいいねを取得
    is_test = False

    if is_test:
        tweets = [
            {"id_str": "2", "text": "hoge",
             "created_at": "Sat Feb 17 12:00:00 +0000 2018"},
            {"id_str": "3", "text": "higi",
             "created_at": "Sun Feb 18 10:00:00 +0000 2018"},
        ]
    else:
        tweets = []
        # 多すぎるとlimitationで止まる
        for page in range(1, 51):
            try:
                tweets_response = twitter.favlist(user_id, page)
            except:
                break
            if tweets_response == []:
                break
            tweets += tweets_response

    # 検索用にtweet_idを配列化
    tweet_ids = [tw["id_str"] for tw in tweets]

    # 登録されてないものを選別
    qs_saved = Like.objects.filter(
        user=user, tweet_id__in=tweet_ids)
    saved_ids = [tw.tweet_id for tw in qs_saved]

    qs_new = [Like.create_item(tw, user) for tw in tweets
              if tw["id_str"] not in saved_ids]

    # DBに記録
    Like.objects.bulk_create(qs_new)
    # return HttpResponse(qs_new)


@login_required
@not_superuser
def record(request, page=1):
    u"""ユーザーのいいねをDBから表示."""
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    user_at = user.access_token

    # likeが登録されていないか古いとDBを更新
    try:
        latest = Like.objects.filter(user=user).latest()
        now = datetime.datetime.now().astimezone(timezone('Asia/Tokyo'))
        elapsed = now - latest.saved_at
    except ObjectDoesNotExist:
        latest = None
    if not latest or elapsed > datetime.timedelta(days=1):
        record_likes(user)

    context = {
    }
    context = list_items(
        request, user_at['user_id'], page,
        lambda p: reverse('favs:record_page', kwargs={'page': p}),
        'like_db', context
    )
    if context["tweets"] == []:
        context['message_required'] = True
        context['messages'] = [
            {"title": "いいねが見つかりません",
             "body": "遡れるツイート数の上限かもしれません。前のページに戻ってください。"},
        ]

    return render(request, template_path('show.html'), context)
