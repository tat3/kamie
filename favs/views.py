from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from . import utils

# Create your views here.

def index(request):
    if 'user_id' in request.session:
        template = loader.get_template('favs/show.html')
    
        twitter = utils.TwitterClient()
        #user_id = '1212759744'
        user_id = request.session['user_id']
        tweets = twitter.add_htmls_embedded(twitter.favlist(user_id))
        context = {
            'user_id': user_id,
            'tweets': tweets,
        }
        print(user_id)
        return HttpResponse(template.render(context, request))

    #return HttpResponseRedirect('login')
    template = loader.get_template('favs/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def show(request, screen_name):
    template = loader.get_template('favs/show.html')
    
    twitter = utils.TwitterClient()
    #user_id = '1212759744'
    user_id = twitter.user_id_from_screen_name(screen_name)
    tweets = twitter.add_htmls_embedded(twitter.favlist(user_id))
    context = {
        'user_id': user_id,
        'tweets': tweets,
    }
    return HttpResponse(template.render(context, request))

def login(request):
    twitter = utils.TwitterClient()
    url = twitter.issue_request_url()
    return HttpResponseRedirect(url)

def logout(request):
    request.session.pop('user_id')
    return HttpResponseRedirect('/')

def callback(request):
    twitter = utils.TwitterClient()
    user_id = twitter.register_access_token(request)
    request.session['user_id'] = user_id
    return HttpResponseRedirect('/')
