import psycopg2

class Database:

    conn = None

    def __init__(self, dbname):
        conn = psycopg2.connect('dbname={}'.format(dbname))

    def save_tweet(id = None, text = None, geo = None, user_id = None, 
        tweet_hashtag_id = None, longitude = None, 
        latitude = None, place_id = None, retweeted_id = None, 
        original_tweet_retweet_count = None, 
        in_reply_to_status_id = None, in_reply_to_user_id = None, 
        lang = None):
        cur = conn.cursor()
        statement = """
        INSERT INTO tweets 
        (id, text, geo, user_id, longitude, latitude, place_id, retweeted_id, original_tweet_retweet_count, in_reply_to_status_id, in_reply_to_user_id, lang) 
        VALUES(%d, %s, %s, %d, %f, %f, %d, %d, %d, %d, %d, %s);
        """
        cur.execute(statement, (id, text, geo, user_id, longitude, latitude, place_id, retweeted_id, original_tweet_retweet_count, in_reply_to_status_id, in_reply_to_user_id, lang))
        
