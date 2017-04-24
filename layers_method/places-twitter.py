import psycopg2

# Returns a bounding box for a tweet
def get_place_bounding_boxes_for_tweet(tweet_id):
    conn = psycopg2.connect('dbname={}'.format('twitter-geo'))
    cur = conn.cursor()
    statement = """
        SELECT min(p.longitude), min(p.latitude), max(p.longitude), max(p.latitude) 
        FROM place_bounding_box_coordinate as p
        INNER JOIN tweets
        USING(place_id)
        WHERE tweets.id = %s
        AND tweets.place_id IS NOT NULL
        GROUP BY place_id
    """
    cur.execute(statement, (tweet_id,))
    conn.commit()
    bounding_boxes = cur.fetchall()
    cur.close()
    result = ()
    if len(bounding_boxes) == 0: return None
    for val in bounding_boxes[0]:
        result = (float(val),) + result
    return result