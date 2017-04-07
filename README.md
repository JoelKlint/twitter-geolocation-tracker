# Todo
- Thread twitter save?
- Webbinterface

# How to setup environment
1. Set these environment variables
```shell
TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET
```
2. Install PostgreSQL
3. Setup database
```shell
$ bash database/setup.sh
```
4. Install python dependencies
```shell
$ pip3 install virtualenv && virtualenv env && source env/bin/activate && pip3 install -r requirements.txt
```

5. Start datamining using your filters
```shell
bash /startup/init.sh start <filter 1> <filter 2> ...
```

6. Check which filters actually allowed by twitter
```shell
bash /startup/init.sh status
```

7. When done, stop the processes with.
```shell
bash /startup/init.sh stop
```
# Antaganden Twitters API
- retweeted_id                  -->     tweeten är en retweet
- in_reply_to_user_id           -->     någon har blivit mentioned
- in_reply_to_status_id         -->     tweeten är ett svar på en annan tweet
- original_tweet_retweet_count  -->     finns bara på kommenterade retweets

- En retweet är en "ren" retweet om attributet "original_tweet_retweet_count" inte är null
- En retweet är en "kommenterad" retweet om attributet "original_tweet_retweet_count" är null


# Statements för att hämta ut statistik
SELECT count(*) FROM tweets WHERE retweeted_id IS NOT NULL AND in_reply_to_status_id IS NOT NULL AND in_reply_to_user_id IS NOT NULL;

SELECT count(*) FROM tweets WHERE retweeted_id IS NOT NULL AND in_reply_to_status_id IS NOT NULL AND in_reply_to_user_id IS NULL;
SELECT count(*) FROM tweets WHERE retweeted_id IS NOT NULL AND in_reply_to_status_id IS NULL AND in_reply_to_user_id IS NOT NULL;
SELECT count(*) FROM tweets WHERE retweeted_id IS NOT NULL AND in_reply_to_status_id IS NULL AND in_reply_to_user_id IS NULL;

SELECT count(*) FROM tweets WHERE retweeted_id IS NULL AND in_reply_to_status_id IS NOT NULL AND in_reply_to_user_id IS NOT NULL;
SELECT count(*) FROM tweets WHERE retweeted_id IS NULL AND in_reply_to_status_id IS NOT NULL AND in_reply_to_user_id IS NULL;
SELECT count(*) FROM tweets WHERE retweeted_id IS NULL AND in_reply_to_status_id IS NULL AND in_reply_to_user_id IS NOT NULL;
SELECT count(*) FROM tweets WHERE retweeted_id IS NULL AND in_reply_to_status_id IS NULL AND in_reply_to_user_id IS NULL;
