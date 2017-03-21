import tweepy
from tweepy.utils import import_simplejson
json = import_simplejson()

class StreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        print("-----")
        data = json.loads(raw_data)

        # Extract tweet info
        id = data.get('id')
        hashtags = data.get('entities', {}).get('hashtags')
        geo = data.get('geo')
        coordinates = data.get('coordinates')
        place = data.get('place')
        #Handle retweets
        retweeted_id = data.get('retweeted_status', {}).get('id')
        if retweeted_id != None:
            original_tweet_retweet_count = data.get('retweeted_status', {}).get('retweet_count')
        else:
            retweeted_id = data.get('quoted_status', {}).get('id')

        # Extract user info
        user = data.get('user')
        user_id = data.get('id')
        user_name = get_info(data, 'name')
        # user_screen_name = get_info(data, 'screen_name')
        # user_location = get_info(data, 'location')
        # user_description = get_info(data, 'description')
        # user_followers_count = get_info(data, 'followers_count')
        # user_friends_count = get_info(data, 'friends_count')
        # user_time_zone = get_info(data, 'time_zone')
        # user_lang = get_info(data, 'lang')
        print(user_id)

        # print(user_screen_name + " " + user_location)