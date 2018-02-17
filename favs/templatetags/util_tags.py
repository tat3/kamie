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
