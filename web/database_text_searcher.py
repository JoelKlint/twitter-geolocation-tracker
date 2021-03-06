from database import Database

class Database(Database):

    def get_total_clean_retweet_count(self):
        cur = self.conn.cursor()

        statement = """
            SELECT count(*)
            FROM tweets
            WHERE text ILIKE 'RT @realDonaldTrump%'
        """

        cur.execute(statement)
        retweet_count = cur.fetchone()

        cur.close()
        return retweet_count[0]
        
    def get_total_commented_retweet_count(self):
        cur = self.conn.cursor()

        statement = """
            SELECT count(*) 
            FROM tweets 
            WHERE text ILIKE '@realDonaldTrump%https://t.co/%'
        """
        cur.execute(statement)
        commented_retweet_count = cur.fetchone()

        cur.close()
        return commented_retweet_count[0]

    def get_total_reply_count(self):
        cur = self.conn.cursor()

        statement = """
            SELECT
                (SELECT count(*)
                FROM tweets
                WHERE text ILIKE '@realDonaldTrump%'
                AND in_reply_to_user_id IN (SELECT user_id FROM trumps_tweets LIMIT 1))
                -
                (SELECT count(*)
                FROM tweets
                WHERE text ILIKE '@realDonaldTrump%https://t.co/%')
            AS total_count
        """
        cur.execute(statement)
        commented_retweet_count = cur.fetchone()

        cur.close()
        return commented_retweet_count[0]

    def get_total_mention_count(self):
        cur = self.conn.cursor()

        statement = """
            SELECT count(*)
            FROM tweets
            WHERE text ILIKE '@realDonaldTrump%'
            AND in_reply_to_user_id NOT IN (SELECT user_id FROM trumps_tweets LIMIT 1)
        """
        cur.execute(statement)
        commented_retweet_count = cur.fetchone()

        cur.close()
        return commented_retweet_count[0]

    def get_original_tweets_count(self):
        cur = self.conn.cursor()

        statement = """
            SELECT count(*)
            FROM tweets
            WHERE user_id = (SELECT user_id FROM trumps_tweets LIMIT 1)
        """
        cur.execute(statement)
        commented_retweet_count = cur.fetchone()

        cur.close()
        return commented_retweet_count[0]

    def get_lost_tweet_ids(self):
        cur = self.conn.cursor()

        statement = """
            SELECT id
            FROM tweets
            WHERE id NOT IN (
                SELECT id
                FROM tweets
                WHERE text ILIKE 'RT @realDonaldTrump%'
            )
            AND id NOT IN (
                SELECT id
                FROM tweets 
                WHERE text ILIKE '@realDonaldTrump%https://t.co/%'
            )
            AND id NOT IN (
                SELECT id
                FROM tweets
                WHERE text ILIKE '@realDonaldTrump%'
                AND in_reply_to_user_id IN (SELECT user_id FROM trumps_tweets LIMIT 1))
                EXCEPT
                SELECT id
                FROM tweets
                WHERE text ILIKE '@realDonaldTrump%https://t.co/%')
            )
            AND id NOT IN (
                SELECT id
                FROM tweets
                WHERE text ILIKE '@realDonaldTrump%'
                AND in_reply_to_user_id NOT IN (SELECT user_id FROM trumps_tweets LIMIT 1)
            )
            AND id NOT IN (
                SELECT id
                FROM tweets
                WHERE user_id = (SELECT user_id FROM trumps_tweets LIMIT 1)
            )
        """

    def select_users_with_predicted_coordinates(self):
        cur = self.conn.cursor()
        statement = """
            SELECT predicted_lat, predicted_long, user_id, user_screen_name
            FROM predicted_user_locations
            INNER JOIN users
            USING(user_id);
        """

        response = []
        cur.execute(statement)
        rows = cur.fetchall()
        for row in rows:
            response.append({
                'lat': float(row[0]),
                'lng': float(row[1]),
                'user_id': str(row[2]),
                'user_screen_name': str(row[3])
            })

        self.conn.commit()
        cur.close()
        return response

    def select_all_users_with_more_then_lang_coordinates(self):
        cur = self.conn.cursor()
        statement = """
        SELECT predicted_lat, predicted_long, user_id, user_screen_name, min(created_at) as created_at, user_time_zone, user_location, preprocessed_location, g.latitude, g.longitude
        FROM  predicted_user_locations
        INNER JOIN users USING(user_id)
        INNER JOIN tweets USING(user_id)
        INNER JOIN identified_via_geonames USING(user_id)
        INNER JOIN geonames as g USING(geonameid)
        WHERE user_id NOT IN (
            SELECT user_id
            FROM users
            WHERE user_lang IS NOT NULL
            AND user_location IS NULL
            AND user_time_zone IS NULL)
        GROUP BY user_id, predicted_lat, predicted_long, user_screen_name, user_time_zone, user_location, preprocessed_location, g.latitude, g.longitude
        ORDER BY created_at ASC;
        """
        response = []
        cur.execute(statement)
        rows = cur.fetchall()
        for row in rows:
            response.append({
                'lat': float(row[0]),
                'lng': float(row[1]),
                'user_id': str(row[2]),
                'user_screen_name': str(row[3]),
                'created_at': str(row[4]),
                'user_time_zone': str(row[5]),
                'user_location': str(row[6]),
                'preprocessed_location': str(row[7]),
                'geonames_latitude': str(row[8]),
                'geonames_longitude': str(row[9]),
            })

        self.conn.commit()
        cur.close()
        return response