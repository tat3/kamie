"""create user model."""
import json

from django.db import models


class BaseTweet(models.Model):
    u"""Tweetモデルのbase class."""

    tweet_id = models.CharField(max_length=128)
    text = models.CharField(max_length=500, blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('social_django.UserSocialAuth',
                             on_delete=models.CASCADE)
    json = models.CharField(max_length=10000, blank=True)

    def __str__(self):
        u"""ツイート内容を返す."""
        return self.text

    def to_dict(self):
        u"""Convert json-text to dict-type object."""
        if self.json == "":
            return {}

        return json.loads(self.json)

    class Meta:
        u"""baseであることを明記."""

        abstract = True
        get_latest_by = "saved_at"


class Fav(BaseTweet):
    u"""アプリ内のお気に入りを管理するテーブル."""


class Like(BaseTweet):
    u"""ユーザーのいいねを保持."""

    created_at = models.DateTimeField()
