import psycopg2
from psycopg2.extensions import AsIs

class Database:


    def __init__(self, db_name):
        self.conn = psycopg2.connect("dbname=" + db_name)


    def selectNumberOfUsers(self):
        cur = self.conn.cursor()
        cur.execute('select count(*) from users;')
        result = cur.fetchone()
        cur.close()
        return result[0]

    def selectAllTables(self):
        cur = self.conn.cursor()
        cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        result_tuple = cur.fetchall()
        result = []
        for row in result_tuple:
            result.append(row[0])
        cur.close()

        return result

    def generateTableData(self, table):
        cur = self.conn.cursor()
        #PRONE FOR SQL INJECTION; DO NOT USE WITH SEARCH FIELDS! ONLY WAY TO DO TABLE SEARCH AS OF NOW
        cur.execute("SELECT * FROM %(table)s LIMIT 1000", {"table": AsIs(table)})
        colnames = [desc[0] for desc in cur.description]
        result_tuple = cur.fetchall()
        cur.close()
        results = {}
        results['table'] = table
        results['cols'] = colnames
        print (results)
        all_tuples = []
        for result in result_tuple:
            res_list = []
            for i in range(len(colnames)):
                res_list.append(result[i])
            all_tuples.append(res_list)
        results['entries'] = all_tuples
        return results


    #Return the number of users that have a timezone
    def nbrOfUsersWithTimeZones(self):
        cur = self.conn.cursor()
        statement ='''
        SELECT count (user_time_zone) from users;
        '''
        cur.execute(statement)
        nbr_of_users = cur.fetchone()
        cur.close()
        return nbr_of_users[0]

    #Return the number of tweets where the user language matches the tweet language.
    def userLangEqualsTweetLang(self):
        cur = self.conn.cursor()
        statement = '''
        select count (*)
        from tweets inner join users using (user_id)
         where users.user_lang = tweets.lang;
        '''
        cur.execute(statement)
        count = cur.fetchone()
        cur.close()
        return count[0];

    #Returns a map of languages and number of users with that language.
    # TODO Räkna ut fördelning för varje språk.
    def nbrOfUsersPerLang(self):
        cur = self.conn.cursor()
        statement = '''
        select user_lang, count(*)
        from users
        group by user_lang;
        '''
        cur.execute(statement)
        result_tuples = cur.fetchall()
        print (result_tuples)
        langs = []
        for lang in result_tuples:
            langs.append({lang[0]: lang[1]})
        return langs

    def nbrOfUsersWithGeoEnable(self):
        cur = self.conn.cursor()
        statement = '''
        select count(*)
        from tweets inner join users using (user_id)
        where geo = true;
        '''
        cur.execute(statement)
        count = cur.fetchone()
        print (count[0])
        return count[0]

    def nbrOfUsersWithLocation(self):
        cur = self.conn.cursor()
        statement = '''
        select count(*)
        from users
        where user_location is not null;
        '''
        cur.execute(statement)
        count = cur.fetchone()
        return count[0]

    def nbrOfTweetsWithPlaces(self):
        cur = self.conn.cursor()
        statement = '''
        select count (*)
        from tweets
        where place_id is not null;
        '''
        cur.execute(statement)
        count = cur.fetchone()
        return count[0]

    def get_total_tweet_count(self):
        cur = self.conn.cursor()

        statement = "SELECT count(*) FROM tweets"
        cur.execute(statement)
        tweet_count = cur.fetchone()

        cur.close()
        return tweet_count[0]

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
            SELECT
                (SELECT count(*)
                FROM tweets
                WHERE text ILIKE '@realDonaldTrump%'
                AND in_reply_to_user_id NOT IN (SELECT user_id FROM trumps_tweets LIMIT 1))
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

