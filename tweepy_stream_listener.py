import tweepy
from tweepy.utils import import_simplejson
json = import_simplejson()

class StreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        print("-----")
        data = json.loads(raw_data)

        # Extract tweet info
        id = data.get('id')
        text = data.get('text')
        hashtags_array = data.get('entities', {}).get('hashtags', [])
        hashtags = []
        for entry in hashtags_array:
            hashtags.append(entry.get('text'))
        geo = data.get('geo')
        longitude = None
        latitude = None
        coordinates = data.get('coordinates')
        if coordinates != None:
            coordinates = coordinates.get('coordinates')
            longitude = coordinates[0]
            latitude = coordinates[1]

        #Handle place data
        place = data.get('place')
        if place != None:
            print(place)
            place_name = place.get('name', None)
            place_country = place.get('country', None)
            place_contry_code = place.get('country_code', None)
            place_url = place.get('url', None)
            place_id = place.get('id', None)
            place_full_name = place.get('full_name', None)
            place_type = place.get('place_type', None)

            attributes = place.get('attributes', None)
            if attributes != None:
                attribute_street_address = attributes.get('street_address', None)
                attribute_locality = attributes.get('locality', None)
                attribute_region = attributes.get('region', None)
                attribute_isothree = attributes.get('iso3', None)
                attribute_postal_code = attributes.get('postal_code', None)

            bounding_box = place.get('bounding_box', None)
            print (bounding_box)
            if bounding_box != None:
                bound_coordinates = bounding_box.get('coordinates', None)
                bound_type = bounding_box.get('type', None)
                if coordinates != None:
                    for coordinate_middleware in coordinates:
                        for coordinate in coordinate_middleware:
                            # INSERT INTO BOUNDING BOX TABLE HERE
                            bound_longitude = coordinate[0]
                            bound_latitude = coordinate[1]


        #Handle retweets
        retweeted_id = data.get('retweeted_status', {}).get('id')
        if retweeted_id != None:
            original_tweet_retweet_count = data.get('retweeted_status', {}).get('retweet_count')
        else:
            retweeted_id = data.get('quoted_status', {}).get('id')
        in_reply_to_status_id = data.get('in_reply_to_status_id')
        in_reply_to_user_id = data.get('in_reply_to_user_id')
        lang = data.get('lang')
        if latitude != None:
            print(longitude)
            print(latitude)

        # Extract user info
        user = data.get('user', {})
        user_id = user.get('id')
        user_name = user.get('name')
        user_screen_name = user.get('screen_name')
        user_location = user.get('location')
        user_description = user.get('description')
        user_followers_count = user.get('followers_count')
        user_friends_count = user.get('friends_count')
        user_time_zone = user.get('time_zone')
        user_lang = user.get('lang')
        user_url = user.get('url')
        user_geo_enabled = user.get('geo_enabled')
