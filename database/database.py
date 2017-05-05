import psycopg2
from shell_arguments import ShellArguments

class Database:

    conn = None
    verbose = False

    def __init__(self, dbname):
        self.conn = psycopg2.connect('dbname={}'.format(dbname))
        self.verbose = ShellArguments.get_args().verbose

    def save_tweet(self,
                   id = None,
                   text = None,
                   geo = None,
                   geo_longitude = None,
                   geo_latitude = None,
                   user_id = None,
                   longitude = None,
                   latitude = None,
                   place_id = None,
                   retweeted_id = None,
                   original_tweet_retweet_count = None,
                   in_reply_to_status_id = None,
                   in_reply_to_user_id = None,
                   lang = None,
                   created_at = None):

        cur = self.conn.cursor()
        statement = """
        INSERT INTO tweets
        (id, text, geo, geo_longitude, geo_latitude, user_id, longitude, latitude, place_id, retweeted_id, original_tweet_retweet_count, in_reply_to_status_id, in_reply_to_user_id, lang, created_at)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(statement, (id, text, geo, geo_longitude, geo_latitude, user_id, longitude, latitude, place_id, retweeted_id, original_tweet_retweet_count, in_reply_to_status_id, in_reply_to_user_id, lang, created_at))
        self.conn.commit()
        cur.close()
        if(self.verbose):
            print('Saving tweet')
            print("""
            id ={0}, text={1}, geo={2}, geo_longitude={3}, geo_latitude={4} user_id={5}, longitude={6}, latitude={7},
            place_id={8}, retweeted_id={9}, original_tweet_retweet_count={10},
            in_reply_to_status_id={11}, in_reply_to_user_id={12}, lang={13}, created_at={14}
            """.format(id, text, geo, geo_longitude, geo_latitude, user_id, longitude, latitude, place_id,
            retweeted_id, original_tweet_retweet_count, in_reply_to_status_id, in_reply_to_user_id, lang, created_at))

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
        if self.verbose:
            print("Saving user")
            print("""
            user_id={0}, user_screen_name={1}, user_name={2}, user_location={3}, user_description={4}, 
            user_followers_count={5}, user_friends_count={6}, user_time_zone={7}, 
            user_lang={8}, user_url={9}, user_geo_enabled={10}
            """.format(user_id, user_screen_name, user_name, user_location, user_description, 
            user_followers_count, user_friends_count, user_time_zone, user_lang, user_url, user_geo_enabled))

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
        if self.verbose:
            print("Updating user")
            print("""
            user_id={0}, user_screen_name={1}, user_name={2}, user_location={3}, user_description={4}, 
            user_followers_count={5}, user_friends_count={6}, user_time_zone={7}, 
            user_lang={8}, user_url={9}, user_geo_enabled={10}
            """.format(user_id, user_screen_name, user_name, user_location, user_description, 
            user_followers_count, user_friends_count, user_time_zone, user_lang, user_url, user_geo_enabled))

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
        if self.verbose:
            print("Saving place")
            print("""
            place_id={0}, place_name={1}, place_country={2}, place_country_code={3}, place_full_name={4}, 
            place_type={5}, place_street_address={6}, place_locality={7}, place_region,={8} 
            place_iso3_country_code={9}, place_postal_code={10}
            """.format(place_id, place_name, place_country, place_country_code, place_full_name, place_type, 
            place_street_address, place_locality, place_region, place_iso3_country_code, place_postal_code))

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
        if self.verbose:
            print("Updating place")
            print("""
            place_id={0}, place_name={1}, place_country={2}, place_country_code={3}, place_full_name={4},
            place_type={5}, place_street_address={6}, place_locality={7}, place_region,={8}
            place_iso3_country_code={9}, place_postal_code={10}
            """.format(place_id, place_name, place_country, place_country_code, place_full_name, place_type,
                       place_street_address, place_locality, place_region, place_iso3_country_code, place_postal_code))
        # print('Place updated')

    def insertBoundingBox(self,
        place_id,
        longitude,
        latitude,
        bound_type):
        cur = self.conn.cursor()
        statement = """
        INSERT INTO place_bounding_box_coordinate
        (place_id, longitude, latitude, bound_type)
        VALUES(%s, %s, %s, %s);
        """
        cur.execute(statement, (place_id, longitude, latitude, bound_type))
        self.conn.commit()
        cur.close
        if self.verbose:
            print("Saving bounding box")
            print("""
            place_id={0}, longitude={1}, latitude={2}, bound_type={3}
            """.format(place_id, longitude, latitude, bound_type))




    def getAllTweetTextAndIds(self):
        cur = self.conn.cursor()
        statement = '''
        SELECT id, text from tweets;
        '''

        cur.execute(statement)
        self.conn.commit()
        textsAndIds = cur.fetchall()
        cur.close()
        return textsAndIds

    def updateDetectedLanguage(self, id, detected_language):
        cur = self.conn.cursor()
        statement = '''
        UPDATE tweets
        SET detected_language = %s
        Where id=%s;
        '''
        data = [detected_language, id]
        cur.execute(statement, data)
        self.conn.commit()
        cur.close()



    def loadCountries(self,
                      geonameid = None,
                      name = None,
                      asciiname = None,
                      alternatenames = None,
                      latitude = None,
                      longitude = None,
                      feature_class = None,
                      feature_code = None,
                      country_code = None,
                      cc2 = None,
                      admin1_code = None,
                      admin2_code = None,
                      admin3_code = None,
                      admin4_code = None,
                      population = None,
                      elevation = None,
                      dem = None,
                      timezone = None,
                      modification_date = None):


        cur = self.conn.cursor()
        statement = """
        INSERT INTO geonames
        (geonameid, name, asciiname, alternatenames, latitude,
        longitude, feature_class, feature_code, country_code,
         cc2, admin1_code, admin2_code, admin3_code, admin4_code,
         population, elevation, dem, timezone, modification_date)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(statement, (geonameid, name, asciiname, alternatenames, latitude, longitude,
                                feature_class, feature_code, country_code,
                                cc2, admin1_code, admin2_code, admin3_code, admin4_code,
                                population, elevation, dem, timezone, modification_date))
        self.conn.commit()
        cur.close()

    def select_user_locations(self):
        cur = self.conn.cursor()
        statement = """
        SELECT user_id, user_location
        FROM users
        WHERE user_location IS NOT NULL;
        """
        cur.execute(statement)
        self.conn.commit()
        result_tuple = cur.fetchall()
        result_array = []
        cur.close()
        for result in result_tuple:
            result_array.append([result[0], result[1]])

        return result_array


    def get_all_users_with_location(self):
        cur = self.conn.cursor()

        statement = """
            SELECT user_id, user_location
            FROM users
            WHERE user_location IS NOT NULL
        """

        cur.execute(statement)
        self.conn.commit()
        result_tuple = cur.fetchall()
        cur.close()

        return result_tuple

    def select_database_locations(self):
        cur = self.conn.cursor()
        statement = """
        SELECT DISTINCT geonameid, name, asciiname, latitude, longitude
        FROM geonames
        WHERE feature_code = 'PPL';
        """
        cur.execute(statement)
        self.conn.commit()
        result_tuple = cur.fetchall()
        result_array = []
        cur.close()
        i = 0
        for result in result_tuple:
            if (i%100000 == 0):
                print("We have selected: ", i)
            result_array.append([result[0], result[1], result[2], float(result[3]), float(result[4])])
            i+=1
        return result_array

    def select_locations_based_on_user_id(self, user_id):
        cur = self.conn.cursor()
        statement = """
        SELECT user_location
        FROM users
        WHERE user_location IS NOT NULL
        AND user_id = %s;
        """
        cur.execute(statement, (user_id,))
        self.conn.commit()
        result_tuple = cur.fetchall()
        result_array = []
        cur.close()
        for result in result_tuple:
            result_array.append([user_id[0], result_tuple[0][0]])

        return result_array

    def set_filtered_location(self, user_id, geonameid, ratio):
        cur = self.conn.cursor()
        statement = """
        INSERT INTO filtered_user_locations(user_id, geonameid, ratio)
        VALUES (%s, %s, %s);
        """
        cur.execute(statement, (user_id, geonameid, ratio))
        self.conn.commit()
        cur.close()


    def insert_into_preprocessed(self, location, user_id, rest=None):
        cur = self.conn.cursor()
        if rest != None:
            statement = """
                UPDATE users
                SET preprocessed_location = %s,
                    preprocessed_rest = %s
                WHERE user_id = %s
            """
            cur.execute(statement, (location, rest, user_id))
        else:
            statement = """
                UPDATE users
                SET preprocessed_location = %s,
                    preprocessed_rest = DEFAULT
                WHERE user_id = %s
            """
        cur.execute(statement, (location, user_id))
        self.conn.commit()
        cur.close()

    def select_preprocessed_data_from_user_id(self, user_id):
        cur = self.conn.cursor()
        statement = '''
        SELECT preprocessed_location, preprocessed_rest FROM users WHERE user_id = %s;
        '''

        cur.execute(statement, ([user_id]))
        self.conn.commit()
        preprocessed_data = cur.fetchone()
        cur.close()
        return preprocessed_data

    def insert_into_identified_via_geonames(self, user_id, geonameid, country_name):
        cur = self.conn.cursor()
        statement = '''
        INSERT INTO identified_via_geonames(user_id, geonameid, country_name)
        VALUES (%s, %s, %s)
        '''

        cur.execute(statement, ([user_id, geonameid, country_name]))
        self.conn.commit()
        cur.close()

    def select_everything_from_users (self):
        cur = self.conn.cursor()
        statement = '''
        SELECT * FROM USERS;
        '''

        cur.execute(statement)
        self.conn.commit()

        data = cur.fetchall()

        cur.close()
        return data

    def select_every_tweet_of_user (self, user_id):
        cur = self.conn.cursor()
        statement = '''
        SELECT * FROM tweets INNER JOIN users using(user_id)
        WHERE user_id = %s;
        '''

        cur.execute(statement, (user_id,))
        self.conn.commit()

        data = cur.fetchall()

        cur.close()
        return data

    def update_predicted_coordinates(self, latitude, longitude, max_value, user_id, error):
        cur = self.conn.cursor()

        statement = '''
        INSERT INTO predicted_user_locations (predicted_lat, predicted_long, max_value, user_id, incorrect) 
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE 
        SET predicted_lat = excluded.predicted_lat, 
            predicted_long = excluded.predicted_long,
            max_value = excluded.max_value;
        '''
        cur.execute(statement, (float(latitude), float(longitude), float(max_value), user_id, error))
        self.conn.commit()
        cur.close()

    def select_users_with_predicted_coordinates(self):
        cur = self.conn.cursor()
        statement = '''
            SELECT * 
            FROM predicted_user_locations
            WHERE predicted_lat <> 0 AND predicted_long <> 0;
            '''

        cur.execute(statement)
        self.conn.commit()

        data = cur.fetchall()

        cur.close()
        return data