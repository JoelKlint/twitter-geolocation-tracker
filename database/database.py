import psycopg2

class Database:

    conn = None

    def __init__(self, dbname):
        self.conn = psycopg2.connect('dbname={}'.format(dbname))

    def save_tweet(self,
                   id = None,
                   text = None,
                   geo = None,
                   user_id = None,
                   longitude = None,
                   latitude = None,
                   place_id = None,
                   retweeted_id = None,
                   original_tweet_retweet_count = None,
                   in_reply_to_status_id = None,
                   in_reply_to_user_id = None,
                   lang = None):

        cur = self.conn.cursor()
        statement = """
        INSERT INTO tweets
        (id, text, geo, user_id, longitude, latitude, place_id, retweeted_id, original_tweet_retweet_count, in_reply_to_status_id, in_reply_to_user_id, lang)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(statement, (id, text, geo, user_id, longitude, latitude, place_id, retweeted_id, original_tweet_retweet_count, in_reply_to_status_id, in_reply_to_user_id, lang))
        self.conn.commit()
        cur.close()
        # print ('Tweet Saved!')

    def tweet_exists(self, tweet_id):
        cur = self.conn.cursor()
        statement = "SELECT id FROM tweets WHERE id = %s"
        data = [tweet_id]
        cur.execute(statement, data)
        
        res = cur.fetchone()
        self.conn.commit()
        cur.close
        return True if res != None else False

    def save_user(self,
        user_id = None,
        user_screen_name = None,
        user_name = None,
        user_location = None,
        user_description = None,
        user_followers_count = None,
        user_friends_count = None,
        user_time_zone = None,
        user_lang = None,
        user_url = None,
        user_geo_enabled = None):

        cur = self.conn.cursor()
        statement = """
        INSERT INTO users
        (user_id, user_screen_name, user_name, user_location, user_description, user_followers_count, user_friends_count, user_time_zone, user_lang, user_url, user_geo_enabled)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(statement, (user_id, user_screen_name, user_name, user_location, user_description, user_followers_count, user_friends_count, user_time_zone, user_lang, user_url, user_geo_enabled))
        self.conn.commit()
        cur.close
        # print ('User Saved!')

    def user_exists(self, user_id):
        cur = self.conn.cursor()
        statement = "SELECT user_id FROM users WHERE user_id = %s"
        data = [user_id]
        cur.execute(statement, data)
        
        res = cur.fetchone()
        self.conn.commit()
        cur.close
        return True if res != None else False
    
    def update_user(self,
        user_id = None,
        user_screen_name = None,
        user_name = None,
        user_location = None,
        user_description = None,
        user_followers_count = None,
        user_friends_count = None,
        user_time_zone = None,
        user_lang = None,
        user_url = None,
        user_geo_enabled = None):

        cur = self.conn.cursor()
        statement = """
            UPDATE users
            SET user_screen_name = %s, 
            user_name = %s, 
            user_location = %s, 
            user_description = %s, 
            user_followers_count = %s, 
            user_friends_count = %s, 
            user_time_zone = %s, 
            user_lang = %s, 
            user_url = %s, 
            user_geo_enabled = %s
            WHERE user_id = %s
        """
        data = [user_screen_name, 
            user_name, 
            user_location, 
            user_description, 
            user_followers_count, 
            user_friends_count, 
            user_time_zone, 
            user_lang, 
            user_url, 
            user_geo_enabled,
            user_id
        ]
        cur.execute(statement, data)
        self.conn.commit()
        cur.close
        # print('User updated')

    def save_place(self,
        place_id = None,
        place_name = None,
        place_country = None,
        place_country_code = None,
        place_full_name = None,
        place_type = None,
        place_street_address = None,
        place_locality = None,
        place_region = None,
        place_iso3_country_code = None,
        place_postal_code = None):

        cur = self.conn.cursor()
        statement = """
        INSERT INTO places
        (place_id, place_name, place_country, place_country_code, place_full_name, place_type, place_street_address, place_locality, place_region, place_iso3_country_code, place_postal_code)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(statement, (place_id, place_name, place_country, place_country_code, place_full_name, place_type, place_street_address, place_locality, place_region, place_iso3_country_code, place_postal_code))
        self.conn.commit()
        cur.close

        # print('Place Saved!')

    def place_exists(self, place_id):
        cur = self.conn.cursor()
        statement = "SELECT place_id FROM places WHERE place_id = %s"
        data = [place_id]
        cur.execute(statement, data)
        
        res = cur.fetchone()
        self.conn.commit()
        cur.close
        return True if res != None else False

    def update_place(self,
        place_id = None,
        place_name = None,
        place_country = None,
        place_country_code = None,
        place_full_name = None,
        place_type = None,
        place_street_address = None,
        place_locality = None,
        place_region = None,
        place_iso3_country_code = None,
        place_postal_code = None):

        cur = self.conn.cursor()
        statement = """
            UPDATE places
            SET place_name = %s, 
            place_country = %s, 
            place_country_code = %s, 
            place_full_name = %s, 
            place_type = %s, 
            place_street_address = %s, 
            place_locality = %s, 
            place_region = %s, 
            place_iso3_country_code = %s, 
            place_postal_code = %s
            WHERE place_id = %s
        """
        data = [place_name, 
            place_country, 
            place_country_code, 
            place_full_name, 
            place_type, 
            place_street_address, 
            place_locality, 
            place_region, 
            place_iso3_country_code, 
            place_postal_code,
            place_id
        ]
        cur.execute(statement, data)
        self.conn.commit()
        cur.close
        # print('Place updated')
