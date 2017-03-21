CREATE TABLE IF NOT EXISTS tweets (
    id INT,
    text TEXT,
    geo TEXT,
    user_id INT,
    tweet_hashtag_id INT,
    longitude FLOAT,
    latitude FLOAT,
    place_id INT,
    retweeted_id INT,
    original_tweet_retweet_count INT,
    in_reply_to_status_id INT,
    in_reply_to_user_id INT,
    lang TEXT,
    PRIMARY KEY (id)
    FOREIGN KEY (place_id) REFERENCES places(place_id)
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    FOREIGN KEY (retweeted_id) REFERENCES tweets(retweeted_id)
)

