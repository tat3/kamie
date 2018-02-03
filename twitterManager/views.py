u"""oauthのテスト."""

from django.shortcuts import render
# from django.urls import reverse

# Create your views here.

# from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth


@login_required
def top_page(request):
    u"""login後にcallbackされたページ."""
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    page_dic = {
        'hoge': 'fuga',
        'user': user
    }
    return render(request, 'twitterManager/top.html', page_dic)
