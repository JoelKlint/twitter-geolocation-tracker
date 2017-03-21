CREATE TABLE IF NOT EXISTS tweets (
    id INT,
    text TEXT,
    geo TEXT,
    coordinates 
    place
    retweeted_id
    original_tweet_retweet_count
    in_reply_to_status_id
    in_reply_to_user_id
    lang
)

CREATE TABLE IF NOT EXISTS users (
    user_id INT,
    user_screen_name TEXT,
    user_name TEXT,
    user_location TEXT,
    user_description TEXT,
    user_followers_count INT, 
    user_friends_count INT,
    user_time_zone TEXT,
    user_lang TEXT,
    user_url TEXT,
    user_geo_enabled BOOLEAN,
    PRIMARY KEY(user_id)
)

CREATE TABLE IF NOT EXISTS user_relations (
    follower_user_id TEXT,
    following_user_id TEXT,
    PRIMARY KEY(follower_user_id, following_user_id),
    FOREIGN KEY(follower_user_id) REFERENCES users(user_id),
    FOREIGN KEY(following_user_id) REFERENCES users(user_id),
)

CREATE TABLE IF NOT EXISTS tweet_hashtags (
    tweet_id INT,
    hashtag TEXT,
    PRIMARY KEY(tweet_id, hashtag),
    FOREIGN KEY(tweet_id) tweets(id)
)