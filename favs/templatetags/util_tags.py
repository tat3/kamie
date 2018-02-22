u"""Util tag functions for template."""

import datetime
from pytz import timezone

from django.template import Library

register = Library()


@register.simple_tag
def created_time(created_at):
    u"""Format datetime string."""
    dt = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    dt = dt.astimezone(timezone('Asia/Tokyo'))
    return dt.strftime('%H:%M - %Y年%m月%d日')


@register.inclusion_tag("favs/_pagination.html", takes_context=True)
def create_paginator(context):
    u"""paginatorを生成する."""
    create_page_url = context["create_page_url"]
    current_page = int(context["page"])
    paginator = [{"page": page,
                  "url": create_page_url(page),
                  "is_current": page == current_page,
                  "name": str(page)}
                 for page in range(current_page - 2, current_page + 3)
                 if page >= 1]
    return {"urls": paginator,
            "paginator_required": context["paginator_required"]}


@register.inclusion_tag("favs/_twitter_btn.html", takes_context=True)
def create_tweet_btn(context):
    u"""ツイートボタンを追加するのに必要な情報."""
    d = {
        "text": "Twitterでいいねした画像ツイートを一覧できるサービス「Kamie Album」",
        "lang": "ja",
        "hashtag": "KamieAlbum",
        "url": context["base_url"],
    }
    param = "hashtags={hashtag}&text={text}&lang={lang}&url={url}".format(**d)
    url = "https://twitter.com/intent/tweet?" + param
    return {"url": url}


@register.inclusion_tag("favs/_message.html", takes_context=True)
def create_flash_message(context):
    u"""必要に応じてメッセージを表示する."""
    if "message_required" not in context:
        context["message_required"] = False
    return context
