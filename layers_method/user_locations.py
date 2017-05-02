import psycopg2

def create_bounding_box(coordinates, padding):
    return [float(coordinates[0])-padding, float(coordinates[1])-padding,
            float(coordinates[0])+padding, float(coordinates[1])+padding]


def get_bounding_box_of_user(user_screen_name):
    conn = psycopg2.connect('dbname={}'.format('twitter-geo'))
    cur = conn.cursor()

    statment = '''
    select longitude, latitude
    from geonames natural join identified_via_geonames natural join users
    where longitude <> 0 and latitude <> 0 and user_screen_name = %s
    limit 1;
    '''

    cur.execute(statment, (user_screen_name,))
    coordinates = cur.fetchone()
    if coordinates == None:
        return None
    cur.close()
    conn.close()
    # Padding the bb with 1 degree
    padding = 1
    return create_bounding_box(coordinates, padding)