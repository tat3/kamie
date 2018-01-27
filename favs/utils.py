from requests_oauthlib import OAuth1Session
import json
import os
import urllib.parse
import threading
from queue import Queue

def merge_two_dicts(a, b):
    return {**a, **b}

class TwitterClient:

    def __init__(self):
        CK = os.environ['tw_ck']
        CS = os.environ['tw_cs']
        AT = os.environ['tw_at']
        AS = os.environ['tw_as']
        self.session = OAuth1Session(CK, CS, AT, AS)

        self.urls = {
            'timeline': 'https://api.twitter.com/1.1/statuses/home_timeline.json',
            'favlist': 'https://api.twitter.com/1.1/favorites/list.json',
            'user': 'https://api.twitter.com/1.1/users/show.json',
            'oembed': 'https://publish.twitter.com/oembed',
        }

    def timeline(self):
        res = self.session.get(self.urls['timeline'], params={})
        if res.status_code != 200: return []
        return json.loads(res.text)
        
    def favlist(self, user_id):
        params = {
            'user_id': user_id,
            'count': 10,
        }
        res = self.session.get(self.urls['favlist'], params=params)
        if res.status_code != 200: return []
        return json.loads(res.text)
    
    def user_from_screen_name(self, screen_name):
        params = {
            'screen_name': screen_name,
        }
        res =  self.session.get(self.urls['user'], params=params)
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
        return user['id_str']

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
    
if __name__ == '__main__':

    user_id = '2355923407'
    screen_name = 'roastedsheep2'
    
    twitter = TwitterClient()    

    user = twitter.user_from_screen_name(screen_name)
    user_id = user['id_str']
    #twitter.show_user(user)

    
    #tweets = twitter.timeline()
    tweets = twitter.favlist(user_id)
    #twitter.show_tweets(tweets)
    tweets = twitter.add_htmls_embedded(tweets)
    print(tweets[0])
