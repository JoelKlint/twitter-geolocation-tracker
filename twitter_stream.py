import os
import sys
import tweepy
from tweepy_stream_listener import StreamListener

# Authenticate
consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
access_token = os.environ["TWITTER_ACCESS_TOKEN"]
access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Build stream connection
api = tweepy.API(auth)
streamListener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=streamListener)

# Create a stream connection
filter_args = sys.argv
filter_args.reverse()
filter_args.pop()
print("Filter is set to: " + str(filter_args))
stream.filter(track=filter_args)