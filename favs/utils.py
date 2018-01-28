from requests_oauthlib import OAuth1Session, OAuth1
import json
import os
import urllib.parse
import threading
from queue import Queue
import requests
from favs.models import User

def merge_two_dicts(a, b):
    return {**a, **b}

class TwitterClient:

    def __init__(self, user_id=''):
        if user_id != '':
            user = User.objects.filter(user_id=user_id)[0]
            self.AT = user.access_token
            self.AS = user.access_token_secret
        else:
            self.AT = os.environ['tw_at']
            self.AS = os.environ['tw_as']

        self.CK = os.environ['tw_ck']
        self.CS = os.environ['tw_cs']

        self.session = OAuth1Session(self.CK, self.CS, self.AT, self.AS)

        self.urls = {
            'timeline': 'https://api.twitter.com/1.1/statuses/home_timeline.json',
            'favlist': 'https://api.twitter.com/1.1/favorites/list.json',
            'user': 'https://api.twitter.com/1.1/users/show.json',
            'oembed': 'https://publish.twitter.com/oembed',
            'request_token': 'https://twitter.com/oauth/request_token',
            'access_token': 'https://twitter.com/oauth/access_token',
            'authorize': 'https://twitter.com/oauth/authorize',
            'account_verified': 'https://api.twitter.com/1.1/account/verify_credentials.json',
        }

    def timeline(self):
        res = self.session.get(self.urls['timeline'], params={})
        if res.status_code != 200: return []
        return json.loads(res.text)
        
    def favlist(self, user_id):
        params = {
            'user_id': user_id,
            'count': 200,
        }
        res = self.session.get(self.urls['favlist'], params=params)
        if res.status_code != 200: return []
        return json.loads(res.text)
    
    def user_from_screen_name(self, screen_name):
        params = {
            'screen_name': screen_name,
        }
        res =  self.session.get(self.urls['user'], params=params)
        print(res.text)
        if res.status_code != 200: return {}
        return json.loads(res.text)
    
    def show_tweets(self, tweets):
        for item in tweets:
            print(item['text'])

    def show_user(self, user):
        print('User ID: {}'.format(user['id_str']))
        print('Screen Name: {}'.format(user['screen_name']))
        print('Name: {}'.format(user['name']))

    def user_id_from_screen_name(self, screen_name):
        user = self.user_from_screen_name(screen_name)
        print(user)
        return user['id_str'] if 'id_str' in user else ''

    def html_embedded(self, tweet, q):
        url = 'https://twitter.com/{screen_name}/status/{tweet_id}'.format(screen_name=tweet['user']['screen_name'], tweet_id=tweet['id_str'])
        params = {
            'url': url,
            'maxwidth': 300,
        }
        res = self.session.get(self.urls['oembed'], params=params)
        if res.status_code != 200: return ''        
        q.put(json.loads(res.text)['html'])

    def add_htmls_embedded(self, tweets):
        threads = []
        queues = []
        for tweet in tweets:
            q = Queue()
            queues.append(q)
            th = threading.Thread(target=self.html_embedded, args=(tweet, q))
            th.start()
            threads.append(th)
        tweets_add = []
        for th, q, tweet in zip(threads, queues, tweets):
            th.join()
            tweet_add = merge_two_dicts(tweet, {'html_embedded': q.get()})
            tweets_add.append(tweet_add)
        
        return tweets_add

    def issue_request_url(self):
        session_auth = OAuth1Session(self.CK, client_secret=self.CS)
        res = session_auth.fetch_request_token(self.urls['request_token'])

        user = User(oauth_token=res['oauth_token'], oauth_secret=res['oauth_token_secret'])
        user.save()

        return session_auth.authorization_url(self.urls['authorize'])

    def register_access_token(self, request):
        oauth_token = request.GET['oauth_token']
        oauth_verifier = request.GET['oauth_verifier']

        user = User.objects.get(oauth_token=oauth_token)
        oauth_secret = user.oauth_secret

        session_auth = OAuth1Session(self.CK, client_secret=self.CS, resource_owner_key=oauth_token, resource_owner_secret=oauth_secret, verifier=oauth_verifier)
        res = session_auth.fetch_access_token(self.urls['access_token'])
        user.access_token = res['oauth_token']
        user.access_secret = res['oauth_token_secret']

        session_user = OAuth1Session(self.CK, self.CS, user.access_token, user.access_secret)
        res = session_user.get(self.urls['account_verified'], params={})
        user_id = json.loads(res.text)['id_str']
        users_old = User.objects.filter(user_id=user_id)
        if len(users_old) >= 1:
            users_old.delete()
        user.user_id = user_id
        user.save()
        return user.user_id
        
if __name__ == '__main__':

    user_id = '1212759744'
    screen_name = 'kemomimi_oukoku'
    
    twitter = TwitterClient()    

    user = twitter.user_from_screen_name(screen_name)
    #user_id = user['id_str']
    twitter.show_user(user)

    
    #tweets = twitter.timeline()
    #tweets = twitter.favlist(user_id)
    #twitter.show_tweets(tweets)
    #tweets = twitter.add_htmls_embedded(tweets)
    #print(tweets[0])

    #print(twitter.issue_request_url())
