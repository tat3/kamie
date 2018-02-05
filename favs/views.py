u"""いいねしたツイートを表示する."""

import os

# from django.shortcuts import render
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
)
from django.template import loader
# from django.urls import reverse
from social_django.models import UserSocialAuth
from . import utils

# Create your views here.

app_name = 'favs'


def template_path(name):
    u"""テンプレートファイル名からにapp_nameを追加."""
    return os.path.join(app_name, name)


def redirect_app_root():
    u"""favsのルートにリダイレクトする."""
    return HttpResponseRedirect(template_path('index'))


def root():
    u"""projectのルートにアクセスされたときfavsのルートにリダイレクトする."""
    return redirect_app_root()


def index(request):
    u"""トップページもしくはユーザーのいいねを表示."""
    if not request.user.is_anonymous:
        template = loader.get_template(template_path('show.html'))
        # user = UserSocialAuth.objects.get(uid=request.session['user_id'])
        user = UserSocialAuth.objects.get(user_id=request.user.id)
        user = user.access_token

        user_id = user['user_id']
        twitter = utils.TwitterClient(
            access_token=user['oauth_token'],
            access_token_secret=user['oauth_token_secret']
        )
        # user_id = '1212759744'
        tweets = twitter.favlist(user_id)
        # print(1)
        tweets = twitter.add_htmls_embedded(tweets)
        # tweets = [item for item in tweets if 'media' in item['entities']]
        context = {
            'user_id': user_id,
            'tweets': tweets,
        }
        # print(user['oauth_token'], user['oauth_token_secret'])
        print(request.user.username)
        return HttpResponse(template.render(context, request))

    # return HttpResponseRedirect('login')
    template = loader.get_template(template_path('index.html'))
    context = {}
    return HttpResponse(template.render(context, request))


def show(request, screen_name):
    u"""指定したユーザーのいいねを表示."""
    template = loader.get_template(template_path('show.html'))

    twitter = utils.TwitterClient()
    # user_id = '1212759744'
    user_id = twitter.user_id_from_screen_name(screen_name)
    if user_id == '':
        return HttpResponseNotFound('<h1>User not found.</h1>')
    tweets = twitter.add_htmls_embedded(twitter.favlist(user_id))
    tweets = [item for item in tweets if 'media' in item['entities']]
    print(tweets[0]['entities']['media'])
    context = {
        'user_id': user_id,
        'tweets': tweets,
    }
    return HttpResponse(template.render(context, request))
