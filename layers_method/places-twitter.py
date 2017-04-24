import psycopg2

def get_place_bounding_boxes_from_db():
    conn = psycopg2.connect('dbname={}'.format('twitter-geo'))
    cur = conn.cursor()
    statement = """
        SELECT min(longitude), min(latitude), max(longitude), max(latitude) 
        FROM place_bounding_box_coordinate 
        GROUP BY place_id
    """
    cur.execute(statement)
    conn.commit()
    bounding_boxes = cur.fetchall()
    cur.close()
    return bounding_boxes