u"""adminページのカスタマイズ."""
from django.contrib import admin

from .models import Fav, Like

# Register your models here.

admin.site.register(Fav)
admin.site.register(Like)
