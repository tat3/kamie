u"""いいねしたツイートを表示する."""

import os
import json

# from django.shortcuts import render
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
)
from django.template import loader, Library
from django.urls import reverse
from social_django.models import UserSocialAuth
from . import utils

from django.contrib.auth.decorators import login_required, user_passes_test
from favs.models import Fav

# Create your views here.

app_name = 'favs'
register = Library()


def template_path(name):
    u"""テンプレートファイル名からにapp_nameを追加."""
    return os.path.join(app_name, name)
    # return app_name + ':' + name


def redirect_favs_root():
    u"""favsのルートにリダイレクトする."""
    return HttpResponseRedirect(template_path('index.html'))


def list_items(request, page, data, create_page_url):
    u"""いいねを表示."""
    template = loader.get_template(template_path('show.html'))

    user_token = {}
    if request.user.is_authenticated:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
        user_token = user.access_token

    twitter = utils.TwitterClient(user=user_token)

    if 'method' not in data:
        return HttpResponseNotFound('<h1>Method was not detected.</h1>')

    if data['method'] == 'like':
        tweets = twitter.favlist(data['user_id'], page)
    elif data['method'] == 'fav':
        favs = Fav.objects.filter(user=user)
        tweets = [twitter.tweet_from_id(fav.tweet_id) for fav in favs]

    tweets = twitter.add_htmls_embedded(tweets)
    tweets = [item for item in tweets if 'media' in item['entities']]
    # print(tweets[0]['entities']['media'])

    url_split = request.build_absolute_uri().split("/")
    base_url = url_split[0] + '//' + url_split[2]

    context = {
        'user': request.user,
        'user_id': data['user_id'],
        'tweets': tweets,
        'create_page_url': create_page_url,
        'page': page,
        'base_url': base_url,
        'is_pc': utils.is_pc(request),
    }
    return HttpResponse(template.render(context, request))


def top_page(request):
    u"""ログインしていない場合のトップページ."""
    return information(request, 'index')


@login_required
@user_passes_test(lambda u: not u.is_superuser)
def index(request, page=1):
    u"""トップページもしくはユーザーのいいねを表示."""
    user = UserSocialAuth.objects.get(user_id=request.user.id).access_token
    data = {
        'user_id': user['user_id'],
        'method': 'like',
    }
    return list_items(request, page, data,
                      lambda p: reverse('favs:index_page', kwargs={'page': p}))


def show(request, screen_name, page=1):
    u"""指定したユーザーのいいねを表示."""
    if request.user.is_anonymous:
        twitter = utils.TwitterClient()
    else:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
        user = user.access_token
        twitter = utils.TwitterClient(user)

    # user_id = '1212759744'
    user_id = twitter.user_id_from_screen_name(screen_name)
    if user_id == '':
        print(twitter.AT, twitter.AS)
        return HttpResponseNotFound('<h1>User not found.</h1>')

    data = {
        'user_id': user_id,
        'screen_name': screen_name,
        'method': 'like',
    }
    return list_items(request, page, data,
                      lambda p: reverse('favs:show_page',
                                        kwargs={'screen_name': screen_name,
                                                'page': p}))


def information(request, name):
    u"""json内の情報を表示する."""
    template = loader.get_template(template_path('{}.html'.format(name)))
    contents = json.load(open('favs/json/{}.json'.format(name), 'r'))
    context = {
        'user': request.user,
        'contents': contents,
        'request': request,
    }
    return HttpResponse(template.render(context, request))


@login_required
@user_passes_test(lambda u: not u.is_superuser)
def account(request, page=1):
    u"""このアプリ上でfavしたツイートを表示."""
    user = UserSocialAuth.objects.get(user_id=request.user.id).access_token
    data = {
        'user_id': user['user_id'],
        'method': 'fav',
    }
    return list_items(request, page, data,
                      lambda p: reverse('favs:account_page',
                                        kwargs={'page': p}))
    # return information(request, 'account')


def contact(request):
    u"""Contact usを表示."""
    return information(request, 'contact')


def about(request):
    u"""About usを表示."""
    res = information(request, 'about')
    print(res.content)
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
    tweet = twitter.tweet_from_id(tweet_id)
    if tweet == {}:
        return HttpResponseNotFound('<h1>Tweet does not exist.</h1>')
    if not Fav.objects.filter(tweet_id=tweet_id, user=user).count() == 0:
        return HttpResponseNotFound('<h1>Tweet is already saved.</h1>')
    fav = Fav(tweet_id=tweet_id, user=user)

    if not confirm:
        fav.save()
        # return HttpResponseRedirect(reverse('favs:index'))
        return HttpResponse("<script>window.close()</script>")

    template = loader.get_template(template_path('save_tweet.html'))
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
    return HttpResponse(template.render(context, request))
