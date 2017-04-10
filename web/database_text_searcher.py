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