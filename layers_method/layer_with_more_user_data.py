import tweepy
import os
import json


def connect_to_api():
    consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    print ('Successfully connected to twitter')

    return tweepy.API(auth)

def tweet_to_map(tweet):
    to_map = json.dumps(tweet._json)
    return json.loads(to_map)

def get_more_tweets(api, user_screen_name):
    return api.user_timeline(user_screen_name)

def filter_important_data(statuses):
    print (0)

def get_language_of_tweet(tweet):
    return tweet.get('lang', None)

def get_user_location_of_tweet(tweet):
    return tweet.get('user', None).get('location', None)

def get_user_time_zone_of_tweet(tweet):
    return tweet.get('user', None).get('time_zone', None)

def get_text_of_tweet(tweet):
    return tweet.get('text', None)

def get_tweet_entities(tweet):
    return tweet.get('entities', None)

def main(user_screen_name):
    api = connect_to_api()
    tweets = get_more_tweets(api, user_screen_name)
    for index, tweet in enumerate(tweets):
        tweet = tweet_to_map(tweet)
        print ('Tweet number:', index, 'have the following properties')
        print ('Text:', get_text_of_tweet(tweet))
        print ('Language:', get_language_of_tweet(tweet))
        print ('Location:', get_user_location_of_tweet(tweet))
        print ('Time Zone:', get_user_time_zone_of_tweet(tweet))
        print ('Entities:', get_tweet_entities(tweet))




main('realDonaldTrump')
