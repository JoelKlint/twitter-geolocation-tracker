import tweepy

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.id)