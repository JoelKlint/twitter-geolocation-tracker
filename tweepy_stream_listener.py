import tweepy
from tweepy.utils import import_simplejson
from database.database import Database
from shell_arguments import ShellArguments
from datetime import datetime
json = import_simplejson()

class StreamListener(tweepy.StreamListener):

    verbose = False

    def __init__(self):
        self.verbose = ShellArguments.get_args().verbose

    def on_data(self, raw_data):
        # print("-----")
        data = json.loads(raw_data)

        # Extract tweet info

        if self.verbose: print ('Running new ')

        print (raw_data)

        db = Database('twitter-geo')

        id = data.get('id')

        # Stop if is not tweet
        if id == None:
            if self.verbose: print('Recieved message that is not a tweet')
            with open('messages-that-are-not-tweets.log', 'a') as log_file:
                log_file.write(datetime.now().__str__() + "\n" + str(raw_data) + "\n\n")
                if self.verbose: print('Saved non-tweet-message to messages-that-are-not-tweets.log')
            return
        
        created_at = data.get('created_at')
        if created_at != None:
            created_at = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        else:
            print('DATE IS NONE FOR TWEET WITH ID {}'.format(id))
            print(raw_data)

        # print(created_at)
        if id == None:
            return 1
        text = data.get('text')
        hashtags_array = data.get('entities', {}).get('hashtags', [])
        hashtags = []
        for entry in hashtags_array:
            hashtags.append(entry.get('text'))
        geo = data.get('geo')
        geo_longitude = None
        geo_latitude = None
        if geo != None:
            print ('Got Geo')
            geo_coordinate = geo.get('coordinates')
            geo = True
            print (geo_coordinate)
            geo_latitude = geo_coordinate[0]
            geo_longitude = geo_coordinate[1]

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


            if db.place_exists(place_id):
                db.update_place(place_id, place_name, place_country, place_full_name, place_type, place_street_address, place_locality, place_region, place_iso3_country_code, place_postal_code)
            else:
                db.save_place(place_id, place_name, place_country, place_full_name, place_type, place_street_address, place_locality, place_region, place_iso3_country_code, place_postal_code)

            bounding_box = place.get('bounding_box', None)
            if bounding_box != None:
                bound_coordinates = bounding_box.get('coordinates', None)
                bound_type = bounding_box.get('type', None)
                if bound_coordinates != None:
                    for coordinate_middleware in bound_coordinates:
                        for coordinate in coordinate_middleware:
                            bound_longitude = coordinate[0]
                            bound_latitude = coordinate[1]
                            db.insertBoundingBox(place_id, bound_longitude, bound_latitude, bound_type)



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

        # Save tweet if it does not exist in database
        if not(db.tweet_exists(id)):
            db.save_tweet(id, text, geo, geo_longitude, geo_latitude, user_id, longitude, latitude, place_id,
                        retweeted_id, original_tweet_retweet_count,
                        in_reply_to_status_id, in_reply_to_user_id, lang, created_at)
