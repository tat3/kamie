u"""oauthのテスト."""

import os

from django.shortcuts import render
# from django.urls import reverse

# Create your views here.

from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from social_django.models import UserSocialAuth

from django.http import (
    HttpResponse,
)
from django.template import loader
from django.urls import reverse

app_name = 'twitterManager'


def template_path(name):
    u"""テンプレートファイル名にapp_nameを追加."""
    return os.path.join(app_name, name)


@login_required
def complete_view(request):
    u"""login後にcallbackされるページ."""
    return HttpResponseRedirect(reverse('favs:index'))

    user = UserSocialAuth.objects.get(user_id=request.user.id)
    page_dic = {
        'user': user,
        'userid': request.user.id,
        'username': request.user.username,
        'first_name': request.user.first_name,
    }
    return render(request, template_path('complete.html'), page_dic)


def login_view(request):
    u"""ログインページを表示するだけ."""
    logout(request)
    template = loader.get_template(template_path('login.html'))
    context = {}
    return HttpResponse(template.render(context, request))


def logout_view(request):
    u"""access_tokenを破棄."""
    logout(request)
    template = loader.get_template(template_path('logout.html'))
    context = {}
    return HttpResponse(template.render(context, request))
