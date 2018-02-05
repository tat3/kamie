u"""twitter apiを叩くクライアントを提供する."""
import json
import os
import threading

from queue import Queue

from requests_oauthlib import OAuth1Session


def merge_two_dicts(a, b):
    """Merge two dicts."""
    c = a.copy()
    c.update(b)
    return c


class TwitterClient:
    u"""クライアントを提供."""

    def __init__(self, access_token="", access_token_secret=""):
        u"""Access tokenがあればそれを使い、なければ自分のものを使ってインスタンスを作成."""
        if access_token != "" and access_token_secret != "":
            self.AT = access_token
            self.AS = access_token_secret
        else:
            self.AT = os.environ['tw_at']
            self.AS = os.environ['tw_as']

        self.CK = os.environ['tw_ck']
        self.CS = os.environ['tw_cs']

        self.session = OAuth1Session(self.CK, self.CS, self.AT, self.AS)

        self.urls = {
            'timeline':
                'https://api.twitter.com/1.1/statuses/home_timeline.json',
            'favlist': 'https://api.twitter.com/1.1/favorites/list.json',
            'user': 'https://api.twitter.com/1.1/users/show.json',
            'oembed': 'https://publish.twitter.com/oembed',
            'request_token': 'https://twitter.com/oauth/request_token',
            'access_token': 'https://twitter.com/oauth/access_token',
            'authorize': 'https://twitter.com/oauth/authorize',
            'account_verified':
                'https://api.twitter.com/1.1/account/verify_credentials.json',
        }

    def timeline(self):
        u"""ユーザー自身のタイムラインを表示."""
        res = self.session.get(self.urls['timeline'], params={})
        if res.status_code != 200:
            return []
        return json.loads(res.text)

    def favlist(self, user_id):
        u"""対称ユーザーのいいね欄を表示."""
        params = {
            'user_id': user_id,
            'count': 20,
        }
        res = self.session.get(self.urls['favlist'], params=params)
        if res.status_code != 200:
            return []
        return json.loads(res.text)

    def user_from_screen_name(self, screen_name):
        u"""ユーザーの@hogeからユーザー情報を返す."""
        params = {
            'screen_name': screen_name,
        }
        res = self.session.get(self.urls['user'], params=params)
        print(res.text)
        if res.status_code != 200:
            return {}
        return json.loads(res.text)

    def show_tweets(self, tweets):
        u"""ツイートのリストを受け取って表示."""
        for item in tweets:
            print(item['text'])

    def show_user(self, user):
        u"""ユーザー情報を受け取って表示."""
        print('User ID: {}'.format(user['id_str']))
        print('Screen Name: {}'.format(user['screen_name']))
        print('Name: {}'.format(user['name']))

    def user_id_from_screen_name(self, screen_name):
        u"""ユーザーの@名からユーザーのid_strを返す."""
        user = self.user_from_screen_name(screen_name)
        print(user)
        return user['id_str'] if 'id_str' in user else ''

    def html_embedded(self, tweet, q):
        u"""Twitter widget用のHTMLを得て、上書きする."""
        # 鍵垢は除外
        if tweet['user']['protected']:
            q.put({})
            return

        url = 'https://twitter.com/{screen_name}/status/{tweet_id}'.format(
            screen_name=tweet['user']['screen_name'], tweet_id=tweet['id_str'])
        params = {
            'url': url,
            'maxwidth': 300,
        }
        res = self.session.get(self.urls['oembed'], params=params)
        if res.status_code != 200:
            return ''
        q.put(json.loads(res.text)['html'])

    def add_htmls_embedded(self, tweets):
        u"""ツイートリストにHTML情報を全て書き込む."""
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
            if tweet['user']['protected']:
                continue
            tweet_add = merge_two_dicts(tweet, {'html_embedded': q.get()})
            tweets_add.append(tweet_add)

        return tweets_add

if __name__ == '__main__':

    user_id = '1212759744'
    screen_name = 'kemomimi_oukoku'

    twitter = TwitterClient()

    user = twitter.user_from_screen_name(screen_name)
    # user_id = user['id_str']
    twitter.show_user(user)

    # tweets = twitter.timeline()
    # tweets = twitter.favlist(user_id)
    # twitter.show_tweets(tweets)
    # tweets = twitter.add_htmls_embedded(tweets)
    # print(tweets[0])

    # print(twitter.issue_request_url())
