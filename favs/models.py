"""create user model."""
import json

from django.db import models

from . import utils


class BaseTweet(models.Model):
    u"""Tweetモデルのbase class."""

    tweet_id = models.CharField(max_length=128)
    text = models.CharField(max_length=500, blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('social_django.UserSocialAuth',
                             on_delete=models.CASCADE)
    json = models.CharField(max_length=10000, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        u"""ツイート内容を返す."""
        return self.text

    def to_dict(self):
        u"""Convert json-text to dict-type object."""
        if self.json == "":
            return {}

        return json.loads(self.json)

    @classmethod
    def create_item(cls, dic, user):
        u"""Save item with dict-type data and user data."""
        tweet = cls(tweet_id=dic["id_str"],
                    text=dic["text"],
                    user=user,
                    json=json.dumps(dic),
                    created_at=utils.parse_datetime(dic["created_at"]))
        return tweet

    class Meta:
        u"""baseであることを明記."""

        abstract = True
        get_latest_by = "saved_at"


class Fav(BaseTweet):
    u"""アプリ内のお気に入りを管理するテーブル."""


class Like(BaseTweet):
    u"""ユーザーのいいねを保持."""
