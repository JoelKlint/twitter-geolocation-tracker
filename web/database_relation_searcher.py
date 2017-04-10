from database import Database

class Database(Database):


#retweeted_id                  -->     tweeten är en retweet
#in_reply_to_user_id           -->     någon har blivit mentioned
#in_reply_to_status_id         -->     tweeten är ett svar på en annan tweet
#original_tweet_retweet_count  -->     finns bara på kommenterade retweets
#En retweet är en "ren" retweet om attributet "original_tweet_retweet_count" inte är null
#En retweet är en "kommenterad" retweet om attributet "original_tweet_retweet_count" är null

#Statements för att hämta ut statistik
#SELECT count(*) FROM tweets WHERE retweeted_id IS NOT NULL AND in_reply_to_status_id IS NOT NULL AND
#SELECT count(*) FROM tweets WHERE retweeted_id IS NOT NULL AND in_reply_to_status_id IS NOT NULL AND
#SELECT count(*) FROM tweets WHERE retweeted_id IS NOT NULL AND in_reply_to_status_id IS NULL AND in_
#SELECT count(*) FROM tweets WHERE retweeted_id IS NOT NULL AND in_reply_to_status_id IS NULL AND in_
#SELECT count(*) FROM tweets WHERE retweeted_id IS NULL AND in_reply_to_status_id IS NOT NULL AND in_
#SELECT count(*) FROM tweets WHERE retweeted_id IS NULL AND in_reply_to_status_id IS NOT NULL AND in_
#SELECT count(*) FROM tweets WHERE retweeted_id IS NULL AND in_reply_to_status_id IS NULL AND in_repl
#SELECT count(*) FROM tweets WHERE retweeted_id IS NULL AND in_reply_to_status_id IS NULL AND in_repl

    def get_total_clean_retweet_count(self):
        cur = self.conn.cursor()

        statement = """
            SELECT count(*) FROM tweets WHERE retweeted_id IS NOT NULL
            AND in_reply_to_status_id IS NULL
            AND in_reply_to_user_id IS NULL;
        """

        cur.execute(statement)
        retweet_count = cur.fetchone()

        cur.close()
        return retweet_count[0]

    def get_total_commented_retweet_count(self):
        cur = self.conn.cursor()

        statement = """
          SELECT count(*) FROM tweets
          WHERE retweeted_id IS NOT NULL
          AND in_reply_to_status_id IS NULL
          AND in_reply_to_user_id IS NOT NULL
        """
        cur.execute(statement)
        commented_retweet_count = cur.fetchone()

        cur.close()
        return commented_retweet_count[0]

    def get_total_reply_count(self):
        cur = self.conn.cursor()

        statement = """
          SELECT count(*) FROM tweets
          WHERE retweeted_id IS NOT NULL
          AND in_reply_to_status_id IS NOT NULL
          AND in_reply_to_user_id IS NOT NULL;
        """
        cur.execute(statement)
        commented_retweet_count = cur.fetchone()

        cur.close()
        return commented_retweet_count[0]

    def get_total_mention_count(self):
        cur = self.conn.cursor()

        statement = """
          select count(*) from tweets
          where in_reply_to_user_id <> 25073877
          AND text ILIKE '@realDonaldTrump%';
        """
        cur.execute(statement)
        commented_retweet_count = cur.fetchone()

        cur.close()
        return commented_retweet_count[0]
