import tweepy
from tweepy.utils import import_simplejson
from database.database import Database
json = import_simplejson()

class StreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        print("-----")
        data = json.loads(raw_data)

        # Extract tweet info


        db = Database('twitter-geo')

        id = data.get('id')
        if id == None:
            return 1
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
        place_id = None
        if place != None:
            print(place)
            place_name = place.get('name', None)
            place_country = place.get('country', None)
            place_contry_code = place.get('country_code', None)
            place_url = place.get('url', None)
            place_id = place.get('id', None)
            place_full_name = place.get('full_name', None)
            place_type = place.get('place_type', None)

            place_street_address = None
            place_locality = None
            place_region = None
            place_iso3_country_code = None
            place_postal_code = None
            attributes = place.get('attributes', None)
            if attributes != None:
                place_street_address = attributes.get('street_address', None)
                place_locality = attributes.get('locality', None)
                place_region = attributes.get('region', None)
                place_iso3_country_code = attributes.get('iso3', None)
                place_postal_code = attributes.get('postal_code', None)

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
            db.save_place(place_id, place_name, place_country, place_full_name, place_type, place_street_address, place_locality, place_region, place_iso3_country_code, place_postal_code)


    #Handle retweets
        retweeted_id = data.get('retweeted_status', {}).get('id')
        original_tweet_retweet_count = None
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

        # print ('About to save')
        # print ('id: ', id, 'text: ', text, 'geo: ', geo, 'user_id: ', user_id, 'longitude: ', longitude,
            #    'latitude: ', latitude, 'place_id: ', place_id,
            #    'retweeted_id: ', retweeted_id, 'Original tweet retweet count: ', original_tweet_retweet_count,
            #    'in reply tweet id: ', in_reply_to_status_id, 'in reply user id: ', in_reply_to_user_id, 'language: ', lang)

        if user_id == None:
            print('GOT NULL')
            print(raw_data)

        # Save user to database
        if db.user_exists(user_id):
            db.update_user(user_id, user_screen_name, user_name, user_location,
                      user_description, user_followers_count, user_friends_count,
                      user_time_zone, user_lang, user_url, user_geo_enabled)
        else:
            db.save_user(user_id, user_screen_name, user_name, user_location,
                      user_description, user_followers_count, user_friends_count,
                      user_time_zone, user_lang, user_url, user_geo_enabled)

        print ('Tweet is original')
        db.save_tweet(id, text, geo, user_id, longitude, latitude, place_id,
                    retweeted_id, original_tweet_retweet_count,
                    in_reply_to_status_id, in_reply_to_user_id, lang)