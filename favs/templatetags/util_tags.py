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
    print(create_page_url(current_page))
    # print([{} for page in range(current_page - 2, current_page + 3)])
    paginator = [{"page": page,
                  "url": create_page_url(page),
                  "is_current": page == current_page,
                  "name": str(page)}
                 for page in range(current_page - 2, current_page + 3)
                 if page >= 1]
    print(paginator)
    return {"urls": paginator}
