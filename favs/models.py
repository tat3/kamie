from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    access_token = models.CharField(max_length=100, unique=True, blank=True)
    access_secret = models.CharField(max_length=100, blank=True)
    oauth_token = models.CharField(max_length=100, unique=True, blank=True)
    oauth_secret = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(blank=True)
