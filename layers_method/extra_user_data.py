import tweepy
import os
import json

#This class connects to the twitter api and gets 20 more tweets and stores them
class Extra_User_Data():

    def __init__(self, user_screen_name):
        api = self.connect_to_api()
        tweets = self.get_more_tweets(api, user_screen_name)
        self.tweets = []
        if tweets:
            for tweet in tweets:
                mapped_tweet = self.tweet_to_map(tweet)
                self.tweets.append(mapped_tweet)


    def connect_to_api(self):
        consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
        consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
        access_token = os.environ["TWITTER_ACCESS_TOKEN"]
        access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    def tweet_to_map(self, tweet):
        to_map = json.dumps(tweet._json)
        return json.loads(to_map)

    def get_more_tweets(self, api, user_screen_name):
        try:
            return api.user_timeline(user_screen_name)
        except tweepy.error.TweepError:
            return False


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


