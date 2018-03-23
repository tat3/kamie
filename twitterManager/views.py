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
    return HttpResponse('<script>window.location.href="/"</script>')
    # return HttpResponseRedirect(reverse('favs:index'))


def login_view(request):
    u"""
    ログインページを表示するだけ.

    現在はトップページから直接ログインするので使わない.
    """
    logout(request)
    template = loader.get_template(template_path('login.html'))
    context = {}
    return HttpResponse(template.render(context, request))


def logout_view(request):
    u"""ログアウトする."""
    logout(request)
    template = loader.get_template(template_path('logout.html'))
    context = {
        # 'user': request.user,
    }
    return HttpResponse(template.render(context, request))
