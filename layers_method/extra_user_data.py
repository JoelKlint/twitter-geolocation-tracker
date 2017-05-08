import tweepy
import os
import json
import requests
import base64


auth_header = None
base_url = "https://api.twitter.com"
#This class connects to the twitter api and gets 20 more tweets and stores them
class Extra_User_Data():

    def __init__(self, user_id):
        print ('Extra user id:', user_id)
        self.authenticate()
        self.tweets = self.get_latest_tweets_by_id(user_id)


    def base64encode(self, string):
        a = string.encode('utf-8')
        b = str(base64.b64encode(a))
        return b.split('\'')[1]

    def authenticate(self):
        global auth_header
        c_key = os.environ["TWITTER_CONSUMER_KEY"]
        c_secret = os.environ["TWITTER_CONSUMER_SECRET"]
        credentials = self.base64encode(c_key + ":" + c_secret)

        url = base_url + "/oauth2/token"
        body = "grant_type=client_credentials"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8.',
            'Authorization': 'Basic {}'.format(credentials)}


        r = requests.post(url, headers=headers, data=body)
        if r.status_code == requests.codes.ok:
            token = r.json()
            bearer = token['access_token']
            auth_header = {'Authorization': 'Bearer {}'.format(bearer)}
            # print('Bearer is {}'.format(bearer))
            return True
        else:
            print('Could not get Twitter API token')
            return False


    def get_latest_tweets_by_id(self, id):
        url = base_url + "/1.1/statuses/user_timeline.json"
        params = {'id': str(id)}
        r = requests.get(url, params=params, headers=auth_header)
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print("Could not get latest tweet")
            return None


    def get_all_tweets(self):
        return self.tweets

    #Use one of the tweets in the array as input!
    def get_language_of_tweet(self, tweet):
        return tweet.get('lang', None)

    def get_user_location_of_tweet(self, tweet):
        return tweet.get('user', None).get('location', None)

    def get_user_time_zone_of_tweet(self, tweet):
        return tweet.get('user', None).get('time_zone', None)

    def get_text_of_tweet(self, tweet):
        return tweet.get('text', None)

    def get_tweet_entities(self, tweet):
        return tweet.get('entities', None)

    def get_tweet_id(self, tweet):
        return tweet.get('id', None)


