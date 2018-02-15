u"""いいねしたツイートを表示する."""

import os

import json
import copy

# from django.shortcuts import render
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
)
from django.template import loader
from django.urls import reverse
from social_django.models import UserSocialAuth
from . import utils

from django.contrib.auth.decorators import login_required
from favs.models import Fav

# Create your views here.

app_name = 'favs'


def template_path(name):
    u"""テンプレートファイル名からにapp_nameを追加."""
    return os.path.join(app_name, name)
    # return app_name + ':' + name


def redirect_favs_root():
    u"""favsのルートにリダイレクトする."""
    return HttpResponseRedirect(template_path('index.html'))


def list(request, page, data):
    u"""いいねを表示."""
    template = loader.get_template(template_path('show.html'))

    if request.user.is_anonymous:
        twitter = utils.TwitterClient()
    else:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
        user = user.access_token
        twitter = utils.TwitterClient(user)

    tweets = twitter.add_htmls_embedded(twitter.favlist(data['user_id'], page))
    tweets = [item for item in tweets if 'media' in item['entities']]
    # print(tweets[0]['entities']['media'])

    def page_url(page):
        if data['name'] == 'index':
            return reverse('favs:index_page',
                           kwargs={'page': max(page, 0)})
        else:
            return reverse('favs:show_page',
                           kwargs={'screen_name': data['screen_name'],
                                   'page': max(page, 0)})

    urls = map(lambda p: {'page': p, 'url': page_url(p), 'name': p},
               range(page - 2, page + 3))
    urls2 = copy.deepcopy(urls)
    context = {
        'user': request.user,
        'user_id': data['user_id'],
        'tweets': tweets,
        'urls': urls,
        'urls2': urls2,
        'page': page,
        'twitter_btn_url': utils.twitter_btn_url(request),
        'is_pc': utils.is_pc(request),
    }
    return HttpResponse(template.render(context, request))


def index(request, page=1):
    u"""トップページもしくはユーザーのいいねを表示."""
    if not request.user.is_anonymous:
        user = UserSocialAuth.objects.get(user_id=request.user.id).access_token
        data = {
            'name': 'index',
            'user_id': user['user_id'],
        }
        return list(request, page, data)

    # loginを強要
    # return HttpResponseRedirect(reverse('twitterManager:login'))

    return information(request, 'index')


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
        'name': 'show',
        'user_id': user_id,
        'screen_name': screen_name,
    }
    return list(request, page, data)


def information(request, name):
    u"""json内の情報を表示する."""
    template = loader.get_template(template_path('{}.html'.format(name)))
    contents = json.load(open('favs/json/{}.json'.format(name), 'r'))
    context = {
        'user': request.user,
        'contents': contents,
    }
    return HttpResponse(template.render(context, request))


def account(request):
    u"""アカウント情報を表示."""
    return information(request, 'account')


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

    user = UserSocialAuth.objects.get(id=request.user.id)
    twitter = utils.TwitterClient(user.access_token)
    tweet = twitter.tweet_from_id(tweet_id)
    if tweet == {}:
        return HttpResponseNotFound('<h1>Tweet does not exist.</h1>')
    fav = Fav(tweet_id=tweet_id, user=user)
    # if not confirm:
    #     fav.save()

    template = loader.get_template(template_path('save_tweet.html'))
    contents = [
        {'title': 'ツイートをお気に入り登録する',
         'body': '良ければ確認ボタンを押してください。'},
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
