u"""いいねしたツイートを表示する."""
# from django.shortcuts import render
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
)
from django.template import loader
from django.urls import reverse

from . import utils

# Create your views here.


def redirect_app_root():
    u"""favsのルートにリダイレクトする."""
    return HttpResponseRedirect(reverse('favs:index'))


def root():
    u"""projectのルートにアクセスされたときfavsのルートにリダイレクトする."""
    return redirect_app_root()


def index(request):
    u"""トップページもしくはユーザーのいいねを表示."""
    if 'user_id' in request.session:
        template = loader.get_template('favs/show.html')

        user_id = request.session['user_id']
        twitter = utils.TwitterClient(user_id=user_id)
        # user_id = '1212759744'
        tweets = twitter.add_htmls_embedded(twitter.favlist(user_id))
        context = {
            'user_id': user_id,
            'tweets': tweets,
        }
        return HttpResponse(template.render(context, request))

    # return HttpResponseRedirect('login')
    template = loader.get_template('favs/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def show(request, screen_name):
    u"""指定したユーザーのいいねを表示."""
    template = loader.get_template('favs/show.html')

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


def login(request):
    u"""OAuthの認証画面にリダイレクト。現在は使用しない."""
    twitter = utils.TwitterClient()
    url = twitter.issue_request_url()
    return HttpResponseRedirect(url)


def logout(request):
    u"""セッションを破棄してログアウト。現在は使用しない."""
    if 'user_id' in request.session:
        request.session.pop('user_id')
    # return HttpResponseRedirect(reverse('favs:index'))
    return redirect_app_root()


def callback(request):
    u"""OAuthの認証からのcallbackを処理し、セッションを開始."""
    twitter = utils.TwitterClient()
    user_id = twitter.register_access_token(request)
    request.session['user_id'] = user_id
    return redirect_app_root()
