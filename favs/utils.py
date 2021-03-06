u"""twitter apiを叩くクライアントを提供する."""
import json
import os
import threading
import datetime
from pytz import timezone

from queue import Queue
from requests_oauthlib import OAuth1Session

# from django.core.paginator import Paginator


def merge_two_dicts(a, b):
    u"""２つの辞書オブジェクトを合体させる."""
    c = a.copy()
    c.update(b)
    return c


class TwitterClient:
    u"""クライアントを提供."""

    def __init__(self, user={}):
        u"""
        Consumer keyとaccess tokenからクライアントを生成する.

        ユーザーがログインしていればその人のトークンを使い、なければ管理者のものを使う.
        """
        if user == {}:
            self.AT = os.environ['tw_at']
            self.AS = os.environ['tw_as']
        else:
            self.AT = user['oauth_token']
            self.AS = user['oauth_token_secret']

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
            'tweet': 'https://api.twitter.com/1.1/statuses/show.json',
        }

    def timeline(self):
        u"""ユーザー自身のタイムラインを表示."""
        res = self.session.get(self.urls['timeline'], params={})
        if res.status_code != 200:
            raise Exception()
        return json.loads(res.text)

    def favlist(self, user_id, page=1, count=100):
        u"""対象ユーザーのユーザーのいいね欄を表示."""
        params = {
            'user_id': user_id,
            'count': count,
            'page': page,
        }
        res = self.session.get(self.urls['favlist'], params=params)
        if res.status_code != 200:
            raise Exception()
        return json.loads(res.text)

    def user_from_screen_name(self, screen_name):
        u"""ユーザーの@hogeからユーザー情報を返す."""
        params = {
            'screen_name': screen_name,
        }
        res = self.session.get(self.urls['user'], params=params)
        if res.status_code != 200:
            raise Exception()
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
        try:
            user = self.user_from_screen_name(screen_name)
        except:
            raise Exception()
        return user['id_str']

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

    def tweet_from_id(self, tweet_id):
        u"""ツイートIDからツイートを取得."""
        params = {
            'id': tweet_id,
        }
        res = self.session.get(self.urls['tweet'], params=params)
        if res.status_code != 200:
            raise Exception()
        return json.loads(res.text)


def is_pc(request):
    u"""ユーザーエージェントからPC or SPを判断."""
    from user_agents import parse
    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)

    return not user_agent.is_mobile
    # return True


def ignore_exceptions(func, items):
    u"""例外を吐かなかったものだけをリスト化して返す."""
    def carry_out(func, item, q):
        u"""一つだけ実行する."""
        try:
            q.put(func(item))
        except:
            q.put(None)

    threads = []
    queues = []
    for item in items:
        q = Queue()
        queues.append(q)
        th = threading.Thread(target=carry_out, args=(func, item, q))
        th.start()
        threads.append(th)
    result = []
    for th, q, item in zip(threads, queues, items):
        th.join()
        res = q.get()
        if res:
            result.append(res)
    print(len(items))
    return result


def parse_datetime(string):
    u"""文字列をパースしてTokyo基準のdatetime型に変換する."""
    dt = datetime.datetime.strptime(string, '%a %b %d %H:%M:%S +0000 %Y')
    return dt.astimezone(timezone('Asia/Tokyo'))

if __name__ == '__main__':

    user_id = '1212759744'
    screen_name = 'kemomimi_oukoku'

    twitter = TwitterClient()

    # user = twitter.user_from_screen_name(screen_name)
    # user_id = user['id_str']
    # twitter.show_user(user)

    # tweets = twitter.timeline()
    tweets = twitter.favlist(user_id)
    # twitter.show_tweets(tweets)
    # tweets = twitter.add_htmls_embedded(tweets)
    print(tweets[0]["favorite_count"])

    # print(twitter.issue_request_url())
