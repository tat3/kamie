from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from utils import TwitterClient

# Create your views here.

def index(request):
    template = loader.get_template('favs/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def show(request, screen_name):
    template = loader.get_template('favs/show.html')
    
    twitter = TwitterClient()
    #user_id = '1212759744'
    user_id = twitter.user_id_from_screen_name(screen_name)
    tweets = twitter.add_htmls_embedded(twitter.favlist(user_id))
    context = {
        'user_id': user_id,
        'tweets': tweets,
    }
    return HttpResponse(template.render(context, request))
