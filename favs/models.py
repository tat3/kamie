"""create user model."""
from django.db import models


class Fav(models.Model):
    u"""アプリ内のお気に入りを管理するテーブル."""

    tweet_id = models.CharField(max_length=128)
    saved_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('social_django.UserSocialAuth',
                             on_delete=models.CASCADE)

    def __str__(self):
        u"""tweet_idを.to_strとして返す."""
        return self.user.access_token.user_id
